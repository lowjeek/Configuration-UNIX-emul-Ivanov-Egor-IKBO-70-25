@echo off
cd /d "%~dp0.."
call run.bat --vfs vfs/broken.xml --script scripts/vfs_basic.txt --config configs/empty.yaml
