TARGET_DIR=".uploads"

FULL_PATH=$(cd "$TARGET_DIR" && pwd)
if [ -d "$TARGET_DIR" ]; then
  echo "Removing files in $FULL_PATH"
  find "$TARGET_DIR" -type f -delete
fi

echo "Creating $TARGET_DIR"
mkdir -p $TARGET_DIR

echo "Saving required dirs file tree in $TARGET_DIR"
tree -I "$TARGET_DIR|testing|__pycache__|*.sh" > "./$TARGET_DIR/filetree.txt"

find . -type f \
  -not -path "./.*" \
  -not -path "./*__pycache__*" \
  -not -name ".kanban" \
  -not -name "LICENSE" \
  -not -name "README.md" \
  -not -name "requirements.txt" \
  -not -path "./testing/*" \
  -not -path "./$TARGET_DIR/*" \
  -not -name "*.sh" | while read -r file; do

  clean_path="${file#./}"
  flat_name="${clean_path//\//.}"

  echo "Copying $clean_path"
  echo "# Original Path: /$clean_path" > "$TARGET_DIR/$flat_name"
  echo "" >> "$TARGET_DIR/$flat_name"
  cat "$file" >> "$TARGET_DIR/$flat_name"
done

echo "DONE"