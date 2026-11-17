#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
command -v swift >/dev/null || { echo '需要 macOS 与 Swift 命令行工具' >&2; exit 1; }
python3 - "$ROOT_DIR" <<'PYFONT'
import sys,json,hashlib
from pathlib import Path
root=Path(sys.argv[1]); folder=root/'resources/fonts/mashanzheng'
expected=json.loads((folder/'provenance.json').read_text())['sha256']
if hashlib.sha256((folder/'MaShanZheng-Regular.ttf').read_bytes()).hexdigest()!=expected:
    raise SystemExit('字体哈希变化，先核对与更新配置，禁止静默换字形')
PYFONT
SEAL_FILE="$(python3 - "$ROOT_DIR" <<'PYSEAL'
import sys,json,hashlib
from pathlib import Path
root=Path(sys.argv[1]);d=json.loads((root/'resources/seals/guyue-b/provenance.json').read_text());p=root/d['path']
if hashlib.sha256(p.read_bytes()).hexdigest()!=d['sha256']:raise SystemExit('独立章哈希漂移，禁止静默换章')
print(p)
PYSEAL
)"
for arg in "$@"; do
  if [[ "$arg" == "--seal-image" ]]; then echo '独立章由固定配置提供，不允许绕过哈希覆盖' >&2; exit 1; fi
done
swift "$SCRIPT_DIR/render_logo.swift" --seal-image "$SEAL_FILE" --font "$ROOT_DIR/resources/fonts/mashanzheng/MaShanZheng-Regular.ttf" "$@"

python3 - "$ROOT_DIR" "$@" <<'PYRECORD'
import sys,json,hashlib
from pathlib import Path
root=Path(sys.argv[1]);args=sys.argv[2:]
values={}
i=0
while i<len(args):
    if args[i]=='--no-seal': i+=1;continue
    if i+1<len(args): values[args[i][2:]]=args[i+1]
    i+=2
if '--help' in args or not args: raise SystemExit(0)
folder=Path(values['output']);p=folder/'render.json';record=json.loads(p.read_text())
for key,file in [('font_sha256',Path(record['font_file'])),('background_sha256',Path(record['background'])),('png_sha256',folder/'logo.png'),('foreground_sha256',folder/'foreground.svg')]:
    record[key]=hashlib.sha256(file.read_bytes()).hexdigest()
if record.get('seal')!='none':
    record['seal_sha256']=hashlib.sha256(Path(record['seal_file']).read_bytes()).hexdigest()
    record['seal_layer_sha256']=hashlib.sha256((folder/'seal-layer.png').read_bytes()).hexdigest()
p.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
PYRECORD
