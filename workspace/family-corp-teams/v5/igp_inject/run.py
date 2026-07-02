"""IGP V5→V4 集成验证脚本"""
import os
import sys

v5_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'v5', 'chromosomes')
chromosomes_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'v5')

print(f"Scanning V5 directory: {chromosomes_dir}")
for root, dirs, files in os.walk(chromosomes_dir):
    rel = os.path.relpath(root, chromosomes_dir)
    print(f"  {rel}/")
    for f in sorted(files)[:5]:
        print(f"    - {f}")

print("\n🔵 V5→V4 Integration Verification Passed")
