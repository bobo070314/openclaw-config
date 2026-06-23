"""Generate 200-line test output for token-saver"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run import compress_output

lines = []
for i in range(200):
    status = "ERROR" if i % 10 == 0 else "WARN" if i % 7 == 0 else "OK"
    lines.append(f"line_{i:04d} | data_{i*7%100:03d} | {status} | payload_{i%50}")

text = "\n".join(lines)
result = compress_output(text)

print(f"Original: {result['original_lines']} lines")
print(f"Compressed: {result['compressed_lines']} lines")
print(f"Errors: {result['error_count']}")
print(f"Warnings: {result['warning_count']}")
print(f"Info: {result['info_count']}")
print()
print(result['compressed_text'])
