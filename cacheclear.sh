mkdir -p ./.pycache_removed

find . -path "./.venv" -prune -o -path "./.pycache_removed" -prune -o -name "__pycache__" -print0 | while IFS= read -r -d '' folder; do

    suffix=$(date +%s%N)
    destname="./.pycache_removed/__pycache__${suffix}"

    echo "Dumping: $folder --> $destname"

    mv "$folder" "$destname"

done