import os
import json
import importlib.util
import sys
from v4_unified_engine import V4UnifiedEngine

def load_module_from_file(file_path):
    spec = importlib.util.spec_from_loader("test_module", None)
    module = importlib.util.module_from_spec(spec)
    with open(file_path, 'r') as f:
        code = f.read()
    exec(code, module.__dict__)
    return module

def run_syntax_check(file_path):
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        compile(code, file_path, 'exec')
        return {"file": file_path, "status": "success", "message": "No syntax errors"}
    except SyntaxError as e:
        return {"file": file_path, "status": "error", "message": str(e)}

def run_code_review(file_path, engine):
    try:
        module = load_module_from_file(file_path)
        review_agent = engine.review_agent
        review_result = review_agent.review(module)
        return {"file": file_path, "review": review_result}
    except Exception as e:
        return {"file": file_path, "review": {"error": str(e)}}

def main():
    engine = V4UnifiedEngine()
    upgrade_dir = "upgrade-v4"
    results = []

    if not os.path.exists(upgrade_dir):
        print(f"Directory {upgrade_dir} does not exist.")
        return

    for filename in os.listdir(upgrade_dir):
        file_path = os.path.join(upgrade_dir, filename)
        if os.path.isfile(file_path) and filename.endswith(".py"):
            syntax_check = run_syntax_check(file_path)
            results.append(syntax_check)

            if syntax_check["status"] == "success":
                review_result = run_code_review(file_path, engine)
                results.append(review_result)

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()