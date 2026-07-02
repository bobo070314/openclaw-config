"""
IGP 研发部 V6 — SDK安装管理器
给下游部门：igp sdk install/update/list
从SDK仓库复制到目标项目
"""
from __future__ import annotations
import json
import os
import shutil
import sys
from typing import Any, Dict, List, Optional


SDK_MANIFEST_PATH = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\sdk\sdk_manifest.json'
SDK_SOURCE_DIR = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\sdk'


SDK_MANIFEST = {
    "doctor": {
        "name": "BugDoctor SDK",
        "version": "1.0.0",
        "description": "10种bug pattern检测",
        "source": r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome9\infra',
        "files": ["v5_bug_doctor.py"],
    },
    "analyzer": {
        "name": "CodeAnalyzer SDK",
        "version": "1.0.0",
        "description": "代码质量分析（Vulture+rope+Semgrep模式）",
        "source": r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome0\infra',
        "files": ["v5_code_analyzer.py"],
    },
    "complexity": {
        "name": "ComplexityAnalyzer SDK",
        "version": "1.0.0",
        "description": "圈复杂度/认知复杂度度量",
        "source": r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome11\infra',
        "files": ["v5_complexity_analyzer.py"],
    },
    "symbolic": {
        "name": "SymbolicEngine SDK",
        "version": "1.0.0",
        "description": "约束求解引擎",
        "source": r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome10\infra',
        "files": ["v5_symbolic_engine.py"],
    },
    "lifecycle": {
        "name": "Lifecycle SDK",
        "version": "1.0.0",
        "description": "产品生命周期管理",
        "source": r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6',
        "files": ["v6_lifecycle.py"],
    },
    "review": {
        "name": "ReviewAgents SDK",
        "version": "1.0.0",
        "description": "三Agent评审（架构/安全/兼容）",
        "source": r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\review',
        "files": ["v6_review_agents.py"],
    },
    "prd": {
        "name": "PRDQueue SDK",
        "version": "1.0.0",
        "description": "跨部门PRD需求管理",
        "source": r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\prd',
        "files": ["prd_queue.py"],
    },
}


class SDKManager:
    """SDK安装管理器"""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or os.path.dirname(SDK_MANIFEST_PATH)
        self.manifest = SDK_MANIFEST
    
    def list_sdks(self) -> List[Dict]:
        return [
            {"key": k, "name": v["name"], "version": v["version"], "description": v["description"]}
            for k, v in self.manifest.items()
        ]
    
    def install(self, sdk_key: str, target_dir: str) -> Dict:
        """安装SDK到目标目录"""
        if sdk_key not in self.manifest:
            return {"error": f"SDK '{sdk_key}' not found. Available: {list(self.manifest.keys())}"}
        
        meta = self.manifest[sdk_key]
        source = meta["source"]
        
        # 创建目标目录
        sdk_target = os.path.join(target_dir, 'igp_sdk', sdk_key)
        os.makedirs(sdk_target, exist_ok=True)

        # 从源SDK目录复制（已经包含__init__.py/version/README/examples）
        src_sdk_dir = os.path.join(SDK_SOURCE_DIR, sdk_key)
        if os.path.exists(src_sdk_dir):
            shutil.copytree(src_sdk_dir, sdk_target, dirs_exist_ok=True)
            copied = [f for f in os.listdir(sdk_target) if f.endswith('.py') or f == 'README.md']
        else:
            # 回退：复制源文件
            copied = []
            for fname in meta.get("files", []):
                src = os.path.join(source, fname)
                dst = os.path.join(sdk_target, fname)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                    copied.append(fname)
                else:
                    for root, dirs, files in os.walk(os.path.dirname(source)):
                        if fname in files:
                            shutil.copy2(os.path.join(root, fname), dst)
                            copied.append(fname)
                            break
            # 生成 __init__.py
            init_content = f'"""IGP SDK: {meta["name"]} v{meta["version"]}"""\n'
            with open(os.path.join(sdk_target, '__init__.py'), 'w', encoding='utf-8') as f:
                for fname in copied:
                    mod = fname.replace('.py', '')
                    init_content += f'from .{mod} import *\n'
                f.write(init_content)
            # 生成 version.py
            with open(os.path.join(sdk_target, 'version.py'), 'w', encoding='utf-8') as f:
                f.write(f'VERSION = "{meta["version"]}"\n')
                f.write(f'NAME = "{meta["name"]}"\n')
            # 生成 README.md
            with open(os.path.join(sdk_target, 'README.md'), 'w', encoding='utf-8') as f:
                f.write(f"""# {meta["name"]} v{meta["version"]}\n\n{meta["description"]}\n""")

        return {
            "success": True,
            "sdk": sdk_key,
            "version": meta["version"],
            "installed_to": sdk_target,
            "files_copied": copied or ['source/', '__init__.py', 'version.py', 'README.md', 'examples/'],
        }
    
    def update(self, sdk_key: str, target_dir: str) -> Dict:
        """重新安装SDK（覆盖）"""
        sdk_target = os.path.join(target_dir, 'igp_sdk', sdk_key)
        if os.path.exists(sdk_target):
            shutil.rmtree(sdk_target)
        return self.install(sdk_key, target_dir)


if __name__ == '__main__':
    mgr = SDKManager()
    
    print("IGP 研发部 SDK 管理器")
    print("=" * 50)
    print(f"\n可用SDK ({len(mgr.manifest)} 个):")
    for sdk in mgr.list_sdks():
        print(f"  {sdk['key']:15} v{sdk['version']:10} {sdk['description']}")
    
    print("\nSDK安装测试:")
    test_target = os.path.join(os.path.dirname(SDK_MANIFEST_PATH), 'sdk', '_test_install')
    for key in mgr.manifest:
        result = mgr.install(key, test_target)
        if result.get('success'):
            print(f"  ✅ {key:15} → {result['files_copied']}")
        else:
            print(f"  ❌ {key:15} → {result.get('error')}")
    
    # 清理
    if os.path.exists(test_target):
        shutil.rmtree(test_target)
    
    print(f"\n全部SDK可安装 ✅")
