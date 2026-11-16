#!/usr/bin/env bash
# Package an explicitly selected, already adapted bitmap for the legacy ICNS route.
set -euo pipefail
if [[ $# -ne 2 ]]; then
  echo '用法：./scripts/export-macos.sh INPUT-1024.png NEW-OUTPUT-DIR' >&2
  exit 2
fi
for tool in sips iconutil python3; do
  command -v "$tool" >/dev/null || { echo "缺少工具：$tool（此导出仅支持 macOS）" >&2; exit 2; }
done
SOURCE_IMAGE="$1"
EXPORT_DIR="$2"
python3 - "$SOURCE_IMAGE" <<'PY'
import struct,sys
from pathlib import Path
p=Path(sys.argv[1]); data=p.read_bytes()
if data[:8] != b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',data[16:24]) != (1024,1024):
    raise SystemExit('仅接受实际 1024×1024 PNG；先按目标重新排版，不盲目缩放或改扩展名')
PY
mkdir -- "$EXPORT_DIR"
mkdir -- "$EXPORT_DIR/AppIcon.iconset"
cp -- "$SOURCE_IMAGE" "$EXPORT_DIR/AppIcon.png"
for entry in '16 icon_16x16' '32 icon_16x16@2x' '32 icon_32x32' '64 icon_32x32@2x' '128 icon_128x128' '256 icon_128x128@2x' '256 icon_256x256' '512 icon_256x256@2x' '512 icon_512x512' '1024 icon_512x512@2x'; do
  read -r dimension icon_name <<< "$entry"
  sips -z "$dimension" "$dimension" "$SOURCE_IMAGE" --out "$EXPORT_DIR/AppIcon.iconset/$icon_name.png" >/dev/null
done
iconutil -c icns "$EXPORT_DIR/AppIcon.iconset" -o "$EXPORT_DIR/AppIcon.icns"
python3 - "$SOURCE_IMAGE" "$EXPORT_DIR" <<'PY'
import sys,json,hashlib
from pathlib import Path
source=Path(sys.argv[1]);out=Path(sys.argv[2])
record={'route':'macos-legacy-icns','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'icns_sha256':hashlib.sha256((out/'AppIcon.icns').read_bytes()).hexdigest(),'iconset_files':len(list((out/'AppIcon.iconset').glob('*.png'))),'warning':'传统位图兼容输出；不是 Icon Composer 图层、未验证 Dock/安装效果、未获用户收录确认'}
(out/'export.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
PY
echo "DRAFT：$EXPORT_DIR/AppIcon.icns（传统 ICNS，不代表已通过平台视觉验收）"
