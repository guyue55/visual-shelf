"""Native preview: fixed alpha aspect, no silent edits outside seal, no overwrite."""
import json
from pathlib import Path
import platform
import shutil
import struct
import subprocess
import tempfile
import unittest
import zlib
ROOT=Path(__file__).resolve().parents[1]

@unittest.skipUnless(platform.system()=='Darwin' and shutil.which('swift'),'需macOS/Swift')
class SealPreviewTests(unittest.TestCase):
    def setUp(self):
        (ROOT/'.drafts').mkdir(exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT/'.drafts');self.folder=Path(self.tmp.name)
        self.base=ROOT/'assets/logos/shared/guyue-yue-logos/personal-identity/shared-guyue-yue-circle-light-v04-png.png'
        self.mask=self.folder/'mask.png'
        self.png(self.mask,False)
    def tearDown(self):self.tmp.cleanup()
    def png(self,file,opaque):
        def chunk(name,data):return struct.pack('>I',len(data))+name+data+struct.pack('>I',zlib.crc32(name+data)&0xffffffff)
        pixels=b''.join(b'\0'+b''.join(bytes((0,0,0,255 if opaque or x==1 else 0)) for x in range(3)) for _ in range(6))
        file.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',3,6,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(pixels))+chunk(b'IEND',b''))
    def run_preview(self,*extra,expected=0):
        cmd=['swift',str(ROOT/'scripts/preview_seal.swift'),'--base',str(self.base),'--approved',str(self.base),'--seal',str(self.mask),'--x','0.825','--y','0.275','--width','0.065','--height','0.145','--color','463A33','--output',str(self.folder/'out'),*extra]
        result=subprocess.run(cmd,capture_output=True,text=True,timeout=45)
        self.assertEqual(result.returncode,expected,result.stdout+result.stderr)
    def test_fixed_alpha_preserves_aspect_and_changes_only_seal_region(self):
        self.run_preview()
        data=json.loads((self.folder/'out/preview.json').read_text())
        self.assertEqual(data['pixels_changed_outside_seal_region'],0)
        self.assertEqual(data['state'],'awaiting-user')
        bounds=data['actual_seal_bounds'];self.assertAlmostEqual(bounds[2]/bounds[3],1/6)
        self.run_preview(expected=1)
    def test_opaque_mask_or_invalid_geometry_rejected(self):
        self.png(self.mask,True);self.run_preview(expected=1)
        self.png(self.mask,False);self.run_preview('--x','nan',expected=1)
    def test_source_extraction_is_pinned_and_reproducible(self):
        import hashlib
        source=ROOT/'assets/logos/product-macrightclick-app-icon-ink-light-b-q96-v01-png.png'
        output=self.folder/'extracted.png'
        cmd=['swift',str(ROOT/'scripts/extract_seal_b.swift'),str(source),str(output)]
        result=subprocess.run(cmd,capture_output=True,text=True,timeout=45)
        self.assertEqual(result.returncode,0,result.stderr)
        first=hashlib.sha256(output.read_bytes()).hexdigest()
        output.unlink()
        repeated=subprocess.run(cmd,capture_output=True,text=True,timeout=45)
        self.assertEqual(repeated.returncode,0,repeated.stderr)
        self.assertEqual(first,hashlib.sha256(output.read_bytes()).hexdigest())
        bad=subprocess.run(cmd[:-2]+[str(self.base),str(self.folder/'bad.png')],capture_output=True,text=True,timeout=45)
        self.assertNotEqual(bad.returncode,0);self.assertFalse((self.folder/'bad.png').exists())

    def test_unrelated_background_change_is_rejected(self):
        other=ROOT/'assets/logos/shared/guyue-yue-logos/personal-identity/shared-guyue-yue-rounded-moonlit-v04-png.png'
        self.run_preview('--base',str(other),expected=1)
        self.assertFalse((self.folder/'out').exists())
