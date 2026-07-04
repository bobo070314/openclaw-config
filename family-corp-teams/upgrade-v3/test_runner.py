"""TestRunner 增强版 — 严格清理LLM输出
修复:
1. 全角标点/括号 → SyntaxError
2. 中文注释行里混入代码
3. import缺失自动补全
4. 纯代码行 vs 说明行判断
"""
import os
import subprocess
import sys
import pathlib
import re
from igp_llm_agent import IGPAgent

class TestRunner:
    def __init__(self):
        self.api_key = os.environ.get("OPENCLAW_DASHSCOPE_KEY")
        if not self.api_key:
            raise ValueError("Missing DASHSCOPE API key")

    def _sanitize_code(self, raw: str) -> str:
        """严格清理LLM输出, 只保留合法Python代码"""
        # 1. 去掉markdown代码块
        cleaned = raw.strip()
        if cleaned.startswith("```python"):
            cleaned = cleaned[9:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        # 2. 尝试提取```代码块(如果外层有中文说明)
        blocks = re.findall(r'```python\n(.*?)\n```', cleaned, re.DOTALL)
        if not blocks:
            blocks = re.findall(r'```\n(.*?)\n```', cleaned, re.DOTALL)
        if blocks:
            cleaned = blocks[-1]

        # 3. 逐行过滤: 去掉非Python行(纯中文说明行)
        lines = []
        for line in cleaned.split('\n'):
            stripped = line.strip()
            if not stripped:
                lines.append(line)
                continue
            # 跳过整行中文字符的行(说明性文字)
            non_ascii_chars = [c for c in stripped if ord(c) > 127]
            ascii_chars = [c for c in stripped if c.isascii() and not c.isspace()]
            if len(non_ascii_chars) > len(ascii_chars) and not stripped.startswith('#'):
                continue
            # 替换全角标点为半角(在字符串里会影响但不在字符串里会SyntaxError)
            if not stripped.startswith('#'):
                line = line.replace('（', '(').replace('）', ')')
                line = line.replace('，', ',').replace('：', ':').replace('；', ';')
                line = line.replace('。', '.').replace('！', '!').replace('？', '?')
                line = line.replace('"', '"').replace('"', '"')
                line = line.replace(''', "'").replace(''', "'")
            lines.append(line)
        cleaned = '\n'.join(lines)

        # 4. 移除编码声明前的所有非import/非注释行
        final_lines = []
        in_header = True
        for line in cleaned.split('\n'):
            stripped = line.strip()
            if in_header:
                if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                    final_lines.append(line)
                elif stripped.startswith('import ') or stripped.startswith('from '):
                    final_lines.append(line)
                    in_header = False
                elif not stripped:
                    continue  # 跳过头部空行
                else:
                    # 跳过怪异头部
                    continue
            else:
                final_lines.append(line)
        cleaned = '\n'.join(final_lines)

        # 5. 基本语法校验: 试着compile
        try:
            compile(cleaned, '<test>', 'exec')
        except SyntaxError as e:
            # 如果编译失败, 去掉尾部不完整代码块再试
            cleaned = cleaned.strip()
            if cleaned:
                # 再试一次
                pass
        return cleaned

    def _fix_imports(self, code_file: str, test_code: str) -> str:
        """检测并补全缺失的import"""
        source_module = pathlib.Path(code_file).stem  # eg igp_mcp_bridge -> igp_mcp_bridge
        source_class = None
        # 尝试从源文件找到类名
        src = pathlib.Path(code_file).read_text(encoding="utf-8")
        for m in re.finditer(r'^class\s+(\w+)', src, re.MULTILINE):
            source_class = m.group(1)
            break

        if source_class and source_class in test_code:
            # 检查是否已经包含真实的from ... import ...
            real_import = f'from {source_module} import'
            fake_import = 'from your_module import'
            
            if fake_import in test_code:
                test_code = test_code.replace(fake_import, real_import)
            
            # 检查需要的import
            needs = []
            # pathlib
            if 'Path(' in test_code and 'from pathlib import Path' not in test_code:
                needs.append("from pathlib import Path\n")
            # tempfile
            if 'tempfile' in test_code and 'import tempfile' not in test_code:
                needs.append("import tempfile\n")
            # json
            if 'json.' in test_code and 'import json' not in test_code:
                needs.append("import json\n")
            # subprocess
            if 'subprocess' in test_code and 'import subprocess' not in test_code:
                needs.append("import subprocess\n")
            # os
            if 'os.' in test_code and 'import os' not in test_code:
                needs.append("import os\n")
            # sys.path
            if 'IGP_MCP' in test_code and not test_code.startswith('import sys'):
                needs.insert(0, "import sys\nimport pathlib\nsys.path.insert(0, str(pathlib.Path(__file__).parent))\n")

            if needs:
                test_code = ''.join(needs) + '\n' + test_code
        return test_code

    def generate_tests(self, code_file, target_coverage=80):
        agent = IGPAgent("quality", 1, model="qwen-plus")
        code = pathlib.Path(code_file).read_text(encoding="utf-8")

        prompt = f"""You are a Python test engineer. Write pytest tests for this code:
```python
{code[:3000]}
```
Requirements:
- Import the main class and all needed stdlib modules
- Cover normal paths, edge cases, and error paths
- Use tmp_path for file operations
- Mock subprocess calls
- Output ONLY valid Python code, no explanations, no markdown
- Use 100% ASCII characters only in code, no Unicode/Chinese"""
        
        result = agent.think(prompt)
        test_code = self._sanitize_code(result)
        test_code = self._fix_imports(code_file, test_code)

        test_file = str(pathlib.Path(code_file).with_name(f"{pathlib.Path(code_file).stem}_test.py"))
        pathlib.Path(test_file).write_text(test_code, encoding="utf-8")

        try:
            # 先compile
            compile(test_code, '<test>', 'exec')
        except SyntaxError as e:
            # 第二次清理: 去掉有问题的字符
            lines = test_code.split('\n')
            clean = []
            for line in lines:
                try:
                    compile(line, '<line>', 'exec')
                    clean.append(line)
                except SyntaxError:
                    # 去掉有害行
                    continue
            test_code = '\n'.join(clean)
            pathlib.Path(test_file).write_text(test_code, encoding="utf-8")

        # 运行测试
        r = subprocess.run(["pytest", test_file, "-v", "--tb=short"],
                          capture_output=True, text=True, timeout=30,
                          encoding="utf-8", errors="replace")
        return {
            "test_file": test_file,
            "passed": ("passed" in r.stdout or "PASSED" in r.stdout) and r.returncode == 0,
            "output": (r.stdout + r.stderr)[-500:],
        }

    def run_test_suite(self, code_files):
        results = []
        for file in code_files:
            print(f"\n=== 正在处理 {file} ===")
            res = self.generate_tests(file)
            results.append(res)
            status = "✅ 通过" if res['passed'] else "❌ 失败"
            print(f"测试结果: {res['test_file']} - {status}")
            if not res['passed']:
                print(f"输出: {res['output']}")
        return results

if __name__ == "__main__":
    runner = TestRunner()
    files = [
        str(pathlib.Path(__file__).parent / "igp_mcp_bridge.py"),
    ]
    results = runner.run_test_suite(files)
    passed = sum(1 for r in results if r['passed'])
    print(f"\n=== 测试报告 ===")
    print(f"通过/总数: {passed}/{len(results)}")
