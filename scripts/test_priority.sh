cd "$(dirname "$0")/.." || exit 1
bash run.sh --vfs vfs/missing.xml --script scripts/fail.txt --config configs/override.yaml
