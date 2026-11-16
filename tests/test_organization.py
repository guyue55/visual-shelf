import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from library import add, build, create_svg, metadata_path, validate
from organization import registry, validate_organization

class OrganizationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        for part in ('catalog','assets','site'):(self.root/part).mkdir()
        (self.root/'site/index.html').write_text('<html></html>')
        self.data={'version':1,'owners':[{'id':'product:reader','name':'阅读器'},{'id':'shared','name':'共享'}],'series':[{'id':'moon','name':'月夜','owner':'product:reader'}],'components':[{'id':'launch','name':'启动'}]}
        (self.root/'organization.json').write_text(json.dumps(self.data))
        self.file=self.root/'sample.svg';self.file.write_text(create_svg('icons','阅','#123456'))
        self.org={'owner':'product:reader','series':'moon','component':'launch','functions':['启动'],'platforms':['macOS']}
    def tearDown(self):self.tmp.cleanup()
    def add(self,**kw):
        args=dict(file=self.file,slug='reader',name='阅',kind='icons',tags=['测试'],source='original',license_name='unknown',author='unknown',description='测试',root=self.root,organization=self.org)
        args.update(kw);return add(**args)
    def test_nested_round_trip_and_real_counts(self):
        item=self.add();self.assertEqual(item['path'],'assets/icons/products/reader/moon/launch/reader.svg')
        self.assertEqual(metadata_path(self.root,'reader').relative_to(self.root).as_posix(),'catalog/products/reader/moon/launch/reader.json')
        self.assertEqual(len(validate(self.root)),1);build(self.root)
        public=json.loads((self.root/'dist/organization.json').read_text());self.assertEqual(public['stats']['products'],1);self.assertEqual(public['series'][0]['count'],1)
    def test_duplicate_id_across_directories_rejected(self):
        self.add();copy=self.root/'catalog/elsewhere/reader.json';copy.parent.mkdir();copy.write_bytes(metadata_path(self.root,'reader').read_bytes())
        with self.assertRaises(ValueError):validate(self.root)
    def test_wrong_series_owner_and_unknown_references(self):
        for delta in ({'owner':'shared'},{'series':'missing'},{'component':'missing'},{'functions':['启动','启动']},{'platforms':[None]}):
            with self.subTest(delta=delta),self.assertRaises(ValueError):validate_organization(dict(self.org,**delta),self.data)
    def test_folder_escape_and_symlink_rejected(self):
        for folder in ('../outside','/tmp/outside','a/../../outside'):
            with self.assertRaises(ValueError):self.add(folder=folder)
        (self.root/'assets/icons').mkdir();(self.root/'assets/icons/link').symlink_to(self.root,target_is_directory=True)
        with self.assertRaises(ValueError):self.add(folder='link/other')
    def test_legacy_flat_metadata_stays_readable(self):
        item=self.add(organization=None);self.assertEqual(item['path'],'assets/icons/reader.svg');self.assertEqual(len(validate(self.root)),1)
    def test_malformed_registry_reports_validation_error(self):
        for data in ([],dict(self.data,owners=[None]),dict(self.data,series=[{'id':'moon','name':'月夜','owner':'missing'}])):
            (self.root/'organization.json').write_text(json.dumps(data))
            with self.assertRaises(ValueError):registry(self.root)
