"""Complexity Module — Code complexity CLI command"""
import sys
import os

def analyze_complexity(file_path):
    """Analyze complexity of a Python file"""
    try:
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'chromosomes', 'chromosome11', 'infra')))
        from v5_complexity_analyzer import ComplexityAnalyzer
        ca = ComplexityAnalyzer()
        result = ca.analyze_file(file_path)
        print(f"Complexity analysis: {file_path}")
        print(f"  Total issues: {result.get('total', 'N/A')}")
        print(f"  Score: {result.get('score', 'N/A')}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(analyze_complexity(sys.argv[1] if len(sys.argv) > 1 else '.'))
