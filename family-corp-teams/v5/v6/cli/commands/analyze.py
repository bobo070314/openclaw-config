"""Analyze Module — Code analysis CLI command"""
import sys
import os

def analyze_code(directory):
    """Run CodeAnalyzer on the specified directory"""
    try:
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'chromosomes', 'chromosome0', 'infra')))
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
        from v5_code_analyzer import CodeAnalyzer
        ca = CodeAnalyzer(directory)
        ca.scan_refactoring()
        ca.scan_bad_patterns()
        ca.scan_mutation_opportunity()
        r = ca.all_results()
        total = sum(len(v) for v in r.values())
        print(f"CodeAnalyzer: {total} issues found")
        for cat, items in r.items():
            if items:
                print(f"  {cat}: {len(items)}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(analyze_code(sys.argv[1] if len(sys.argv) > 1 else '.'))
