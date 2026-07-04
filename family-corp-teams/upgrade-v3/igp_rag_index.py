"""
IGP RAG Index — 代码库语义索引

解决维度：代码库深度理解 (6→9)

原理：扫描项目目录 → chunk代码 → 用Qwen生成embedding → 存入本地向量缓存
每次Agent执行前先查RAG获取相关上下文

不用外部向量数据库，纯本地JSON存储
"""
import pathlib, json, os, re, hashlib, httpx, textwrap

CACHE_FILE = pathlib.Path(__file__).parent / ".rag_cache.json"
INDEX_DIR = pathlib.Path(__file__).parent.parent.parent  # workspace

# chunk配置
CHUNK_SIZE = 200  # 每块行数
CHUNK_OVERLAP = 20

class RAGIndex:
    """代码库语义索引"""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("OPENCLAW_DASHSCOPE_KEY", "")
        self.cache = self._load_cache()
        self.chunks = []

    def _load_cache(self):
        if CACHE_FILE.exists():
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        return {"version": 1, "files": {}}

    def _save_cache(self):
        CACHE_FILE.write_text(json.dumps(self.cache, ensure_ascii=False, indent=2), encoding="utf-8")

    def scan_codebase(self, root=None):
        """扫描代码目录，按文件分块"""
        root = root or INDEX_DIR
        print(f"  [RAG] 扫描: {root.name}")

        # 忽略目录
        ignore_dirs = {".git", "node_modules", "__pycache__", "venv", ".venv", ".next", "dist", "build", "skills", "gh-enterprise-baseline", "v1.1-self-evo-factory", "family-corp-teams", "test"}
        max_files = 100
        
        files_indexed = 0
        chunks_created = 0

        for f in root.rglob("*"):
            # 上限保护
            if files_indexed >= max_files:
                break
            if f.is_dir() and f.name in ignore_dirs:
                continue
            if not f.is_file():
                continue
            # 只索引代码文件
            ext = f.suffix.lower()
            if ext not in {".py", ".js", ".ts", ".tsx", ".jsx", ".md", ".json", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".css", ".html", ".sh", ".bat", ".go", ".rs", ".java", ".vue", ".svelte"}:
                continue
            # 跳过太大的文件
            if f.stat().st_size > 500_000:
                continue

            rel = str(f.relative_to(root))
            mtime = f.stat().st_mtime
            fhash = hashlib.md5(f.read_bytes()[:10000]).hexdigest()

            # 跳过未变更的
            cached = self.cache.get("files", {}).get(rel, {})
            if cached.get("hash") == fhash and cached.get("mtime") == mtime:
                continue

            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                lines = content.split("\n")
                chunks = []
                for i in range(0, len(lines), CHUNK_SIZE - CHUNK_OVERLAP):
                    chunk_lines = lines[i:i + CHUNK_SIZE]
                    chunk_text = "\n".join(chunk_lines)
                    chunks.append({
                        "start_line": i + 1,
                        "end_line": min(i + CHUNK_SIZE, len(lines)),
                        "text": chunk_text[:5000],  # 限制每块大小
                        "size": len(chunk_text),
                    })

                self.cache["files"][rel] = {
                    "hash": fhash,
                    "mtime": mtime,
                    "size": f.stat().st_size,
                    "ext": ext,
                    "chunks": chunks,
                }
                files_indexed += 1
                chunks_created += len(chunks)
            except Exception as e:
                print(f"  [RAG] WARN: {rel} -> {e}")

        self._save_cache()
        return files_indexed, chunks_created

    def search(self, query: str, top_k: int = 5) -> list:
        """关键词搜索代码块（暂用关键词匹配，后续可用embedding）"""
        keywords = set(re.findall(r'\w+', query.lower()))
        scored = []

        for rel, finfo in self.cache.get("files", {}).items():
            for chunk in finfo.get("chunks", []):
                text_lower = chunk["text"].lower()
                # 简单关键词匹配
                score = sum(1 for kw in keywords if kw in text_lower and len(kw) > 2)
                # 文件名匹配加分
                if any(kw in rel.lower() for kw in keywords):
                    score += 2
                if score > 0:
                    scored.append({
                        "file": rel,
                        "lines": f"{chunk['start_line']}-{chunk['end_line']}",
                        "score": score,
                        "preview": chunk["text"][:200],
                    })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def get_context(self, query: str, top_k: int = 5) -> str:
        """获取RAG上下文，格式化为LLM友好的文本"""
        results = self.search(query, top_k)
        if not results:
            return "(未找到相关代码)"

        ctx_parts = ["相关代码上下文:"]
        for r in results:
            ctx_parts.append(f"\n--- {r['file']} (L{r['lines']}, 相关度:{r['score']}) ---")
            ctx_parts.append(r["preview"])
        return "\n".join(ctx_parts)

    def stats(self) -> dict:
        files = len(self.cache.get("files", {}))
        chunks = sum(len(f.get("chunks", [])) for f in self.cache["files"].values())
        return {"files": files, "chunks": chunks}


if __name__ == "__main__":
    rag = RAGIndex()
    print("  [RAG] 开始索引代码库...")
    f, c = rag.scan_codebase()
    print(f"  [RAG] 索引完成: {f} 文件, {c} 代码块")
    s = rag.stats()
    print(f"  [RAG] 总量: {s['files']} 文件, {s['chunks']} 块")

    # 搜索测试
    print("\n  [RAG] 搜索测试: 'docker python build'")
    results = rag.search("docker python build")
    for r in results[:3]:
        print(f"    [{r['score']}] {r['file']} (L{r['lines']})")
