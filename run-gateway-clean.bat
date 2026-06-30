@echo off
cd /d D:\bobo\openclaw-foreign
node openclaw\openclaw.mjs gateway --port 18900 > "D:\bobo\openclaw-foreign\logs\startup-clean.log" 2>&1