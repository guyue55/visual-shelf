import argparse
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import studio
from library import add,create_svg,validate
import library


class StudioTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        for name in ('catalog','assets','templates/visual'):
            (self.root/name).mkdir(parents=True)
        self.source=self.root/'reference.svg'; self.source.write_text(create_svg('icons','x','#123456'))
        add(self.source,'source-icon','来源','icons',['参考'],'original','unknown','unknown','test',root=self.root)
        (self.root/'templates/visual/styles.json').write_text(json.dumps({'moonlit-blue':{'name':'test','reference':'source-icon','direction':'test'}}))
        self.patch=patch.object(studio,'ROOT',self.root); self.patch.start()
        studio.prepare(argparse.Namespace(job='test-job',style='moonlit-blue',purpose='cover',text='手记',owner='unknown',instructions=''))
        self.candidate=self.root/'new.svg'; self.candidate.write_text(create_svg('icons','x','#654321'))

    def tearDown(self):
        self.patch.stop(); self.tmp.cleanup()

    def review(self):
        studio.review(argparse.Namespace(job='test-job',file=self.candidate,checks='测试夹具，非真人视觉验收',tool='unit-test'))

    def args(self):
        task=json.loads((self.root/'.drafts/test-job/task.json').read_text())
        return argparse.Namespace(job='test-job',sha256=task.get('candidate_sha256',''),approval='测试夹具确认',id='new-cover',name='封面',owner='product:test',family='test-cover',variant='color',revision='v01',tags='测试',license='unknown',author='unknown',description='test')

    def test_prepare_only_creates_private_copy(self):
        self.assertEqual(len(list((self.root/'catalog').glob('*.json'))),1)
        task=json.loads((self.root/'.drafts/test-job/task.json').read_text())
        self.assertEqual((task['seal'],task['font'],task['profile']),('古月','MaShanZheng-Regular','cover'))
        self.assertEqual((self.root/'.drafts/test-job/reference.svg').read_bytes(),self.source.read_bytes())

    def test_accept_before_review_rejected(self):
        with self.assertRaises(ValueError): studio.accept(self.args())

    def test_empty_confirmation_rejected(self):
        self.review(); args=self.args(); args.approval=' '
        with self.assertRaises(ValueError): studio.accept(args)

    def test_candidate_change_invalidates_review(self):
        self.review(); args=self.args()
        (self.root/'.drafts/test-job/candidate.svg').write_text(create_svg('icons','x','#abcdef'))
        with self.assertRaises(ValueError): studio.accept(args)

    def test_confirmed_candidate_imports_once_with_receipt(self):
        self.review(); args=self.args(); studio.accept(args)
        item=json.loads((self.root/'catalog/new-cover.json').read_text())
        self.assertEqual(item['approval']['reviewed_sha256'],item['sha256'])
        with self.assertRaises(ValueError): studio.accept(args)

    def test_unknown_owner_blocks_accept_but_not_prepare(self):
        self.review(); args=self.args(); args.owner='unknown'
        with self.assertRaises(ValueError): studio.accept(args)

    def test_approved_asset_change_requires_new_confirmation(self):
        self.review(); studio.accept(self.args())
        meta=self.root/'catalog/new-cover.json'
        item=json.loads(meta.read_text())
        file=self.root/item['path']
        file.write_text(create_svg('icons','x','#abcdef'))
        item['sha256']=studio.digest(file)
        meta.write_text(json.dumps(item))
        with self.assertRaisesRegex(ValueError,'用户确认'):
            validate(self.root)

    def test_reference_is_not_a_new_output(self):
        self.candidate.write_bytes(self.source.read_bytes())
        with self.assertRaises(ValueError): self.review()

    def test_create_cli_only_writes_draft(self):
        argv=['library.py','create','--id','created-draft','--name','草稿','--kind','covers','--tags','测试']
        with patch.object(library,'ROOT',self.root), patch.object(sys,'argv',argv):
            library.main()
        self.assertTrue((self.root/'.drafts/created-draft/template.svg').exists())
        self.assertFalse((self.root/'catalog/created-draft.json').exists())

    def test_add_cli_requires_user_confirmation(self):
        argv=['library.py','add',str(self.candidate),'--id','test-add','--name','test','--kind','icons','--tags','test','--source','original','--license','unknown']
        with patch.object(sys,'argv',argv), self.assertRaises(SystemExit) as error:
            library.main()
        self.assertEqual(error.exception.code,2)

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError): studio.job_dir('../outside')
