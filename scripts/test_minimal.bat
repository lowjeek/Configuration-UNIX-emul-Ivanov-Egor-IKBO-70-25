@echo off
cd /d "%~dp0.."
call run.bat --vfs vfs/minimal.xml --script scripts/vfs_basic.txt --config configs/empty.yaml
