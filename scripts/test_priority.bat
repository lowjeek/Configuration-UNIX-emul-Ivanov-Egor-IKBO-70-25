@echo off
cd /d "%~dp0.."
call run.bat --vfs vfs/missing.xml --script scripts/fail.txt --config configs/override.yaml
