"""
IGP Semantic RAG — Qwen embedding语义代码搜索

吸收自 Claude Code/Cursor 上下文引擎:
- 代码分块 + Qwen embedding向量化
- 语义搜索 (非关键词)
- 自动增量索引
"""
import pathlib, json, hashlib, httpx, os, re

class SemanticRAG:
    """语义代码索引 (用Qwen embedding)"""
    
    EMBED_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings"
    
    def __init__(self):
        self.api_key = os.environ.get("OPENCLAW_DASHSCOPE_KEY", "")
        self.cache_file = pathlib.Path(__file__).parent / ".semantic_rag.json"
        self.cache = self._load()
    
    def _load(self):
        if self.cache_file.exists():
            return json.loads(self.cache_file.read_text(encoding="utf-8"))
        return {"version": 2, "embeddings": []}
    
    def embed(self, text):
        """调用Qwen embedding"""
        resp = httpx.post(
            self.EMBED_URL,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"model": "text-embedding-v3", "input": text[:2048]},
            timeout=30
        )
        if resp.status_code == 200:
            return resp.json()["data"][0]["embedding"]
        return []
    
    def search(self, query, top_k=5):
        """语义搜索(余弦相似度)"""
        import math
        q_vec = self.embed(query)
        if not q_vec:
            return []
        scored = []
        for item in self.cache["embeddings"]:
            vec = item["embedding"]
            dot = sum(a*b for a,b in zip(q_vec, vec))
            na = math.sqrt(sum(a*a for a in q_vec))
            nb = math.sqrt(sum(b*b for b in vec))
            sim = dot / (na * nb + 1e-10) if na and nb else 0
            scored.append({"file": item["file"], "content": item["content"], "score": sim})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
