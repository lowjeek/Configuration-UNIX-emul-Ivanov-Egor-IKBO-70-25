@echo off
cd /d "%~dp0.."
call run.bat --vfs vfs/minimal.xml --script scripts/success.txt --config configs/empty.yaml
