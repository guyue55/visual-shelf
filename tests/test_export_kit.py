import importlib.util
from pathlib import Path
import struct
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('export_kit',ROOT/'scripts/export-kit.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class ICOTests(unittest.TestCase):
    def test_empty_rejected(self):
        with self.assertRaises(ValueError):module.ico_from_pngs([])
    def test_binary_offsets_match_png_frames(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            files=[]
            for size in [16,32,48]:
                p=Path(tmp)/f'{size}.png'
                p.write_bytes(b'\x89PNG\r\n\x1a\n'+b'\x00'*8+struct.pack('>II',size,size)+b'fixture')
                files.append(p)
            data=module.ico_from_pngs(files)
            self.assertEqual(struct.unpack('<HHH',data[:6]),(0,1,3))
            for index,size in enumerate([16,32,48]):
                w,h,_,_,planes,bits,length,offset=struct.unpack('<BBBBHHII',data[6+index*16:22+index*16])
                self.assertEqual((w,h,planes,bits),(size,size,1,32))
                self.assertEqual(data[offset:offset+length],files[index].read_bytes())
    def test_wrong_format_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'x.png';p.write_bytes(b'not-png')
            with self.assertRaises(ValueError):module.ico_from_pngs([p])
