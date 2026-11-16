import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from library import add, build, check_svg, create_svg, validate


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / 'catalog').mkdir()
        (self.root / 'assets').mkdir()
        (self.root / 'site').mkdir()
        (self.root / 'site' / 'index.html').write_text('<html></html>')
        self.file = self.root / 'sample.svg'
        self.file.write_text(create_svg('icons', '完成', '#123456'))

    def tearDown(self):
        self.tmp.cleanup()

    def add(self, **overrides):
        args = dict(file=self.file, slug='test-icon', name='图标', kind='icons', tags=['测试'], source='original', license_name='unknown', author='unknown', description='测试', root=self.root)
        args.update(overrides)
        return add(**args)

    def test_import_validate_build_and_rebuild(self):
        self.add()
        self.assertEqual(len(validate(self.root)), 1)
        build(self.root); build(self.root)
        records = json.loads((self.root / 'dist' / 'catalog.json').read_text())
        self.assertEqual(records[0]['id'], 'test-icon')
        self.assertEqual((self.root / 'dist' / records[0]['path']).read_bytes(), self.file.read_bytes())

    def test_duplicate_rejected_without_overwrite(self):
        self.add()
        with self.assertRaises(ValueError):
            self.add(slug='another')
        self.assertFalse((self.root / 'catalog' / 'another.json').exists())

    def test_invalid_metadata_leaves_no_asset(self):
        for fields in ({'source':'javascript:alert(1)'}, {'tags':[]}, {'name':''}, {'slug':'../escape'}):
            with self.assertRaises(ValueError):
                self.add(**fields)
        self.assertEqual(list((self.root / 'catalog').iterdir()), [])
        self.assertEqual(list((self.root / 'assets').iterdir()), [])

    def test_hash_drift_detected(self):
        record = self.add()
        (self.root / record['path']).write_text(create_svg('icons', '完成', '#654321'))
        with self.assertRaisesRegex(ValueError, '哈希'):
            validate(self.root)

    def test_orphan_detected(self):
        (self.root / 'assets' / 'orphan.svg').write_bytes(self.file.read_bytes())
        with self.assertRaisesRegex(ValueError, '未登记'):
            validate(self.root)

    def test_path_escape_detected(self):
        self.add()
        meta = self.root / 'catalog' / 'test-icon.json'
        record = json.loads(meta.read_text())
        record['path'] = '../sample.svg'
        meta.write_text(json.dumps(record))
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_symlink_rejected(self):
        link = self.root / 'linked.svg'
        link.symlink_to(self.file)
        with self.assertRaisesRegex(ValueError, '普通文件'):
            self.add(file=link)

    def test_generated_titles_escaped_and_all_templates_valid(self):
        for kind in ('icons','covers','legends'):
            svg = create_svg(kind, '<script>& title', '#123456', '<hi>')
            check_svg(svg.encode())
            self.assertNotIn('<script>', svg)

    def test_svg_active_content_external_refs_and_invalid_boxes_rejected(self):
        contents = ['<script>alert(1)</script>', '<g onclick="alert(1)"/>', '<foreignObject/>', '<image href="https://example.com/a.png"/>', '<rect fill="url(https://example.com/a)"/>', '<style>@import "x";</style>', '<set attributeName="fill"/>', '<g style="fill:red"/>']
        for content in contents:
            with self.subTest(content=content), self.assertRaises(ValueError):
                check_svg(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">{content}</svg>'.encode())
        for box in ('0 0 -1 64','0 0 nan 64','0 0 inf 64','0 0 0 0'):
            with self.assertRaises(ValueError):
                check_svg(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}"/>'.encode())
        with self.assertRaises(ValueError):
            check_svg(b'<!DOCTYPE svg><svg/>')

    def test_raster_extension_mismatch(self):
        file = self.root / 'fake.png'
        file.write_bytes(self.file.read_bytes())
        with self.assertRaisesRegex(ValueError, '格式'):
            self.add(file=file)


if __name__ == '__main__':
    unittest.main()
