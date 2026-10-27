cd "$(dirname "$0")/.." || exit 1
bash run.sh --vfs vfs/minimal.xml --script scripts/success.txt --config configs/empty.yaml
