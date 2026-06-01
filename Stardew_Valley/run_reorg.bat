@echo off
chcp 65001 > nul
cd /d "%~dp0"
python reorganize_items.py > output_log.txt 2>&1
type output_log.txt