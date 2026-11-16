#!/usr/bin/env python3
"""Verify this delivery without installing any dependency or running artwork code."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


def verify(root):
    root = Path(root).resolve()
    manifest = root / 'package.json'
    if manifest.is_symlink():
        raise ValueError('清单不允许符号链接')
    data = json.loads(manifest.read_text(encoding='utf-8'))
    if data.get('version') != 1 or not isinstance(data.get('files'), dict) or not data['files']:
        raise ValueError('不支持或为空的交付清单')
    checksum = hashlib.sha256(json.dumps(data['files'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    if checksum != data.get('inventory_sha256'):
        raise ValueError('清单校验值变化')
    expected = set(data['files']) | {'package.json'}
    actual = set()
    for file in root.rglob('*'):
        if file.is_symlink():
            raise ValueError('不允许符号链接')
        if file.is_file():
            actual.add(file.relative_to(root).as_posix())
    if actual != expected:
        raise ValueError(f'文件集合变化：缺少 {sorted(expected-actual)}；多出 {sorted(actual-expected)}')
    for name, info in data['files'].items():
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name or path.as_posix() != name:
            raise ValueError('清单路径越界或不规范')
        file = root / name
        if file.stat().st_size != info['bytes'] or hashlib.sha256(file.read_bytes()).hexdigest() != info['sha256']:
            raise ValueError(f'文件变化：{name}')
    return data


if __name__ == '__main__':
    try:
        result = verify(Path(__file__).resolve().parent)
        print(f"VERIFIED：{result['id']}；{len(result['files'])} 个受检文件；{result['state']}")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'校验失败：{exc}', file=sys.stderr)
        sys.exit(1)
