"""Portable delivery safety and selection; no native renderer required."""
import argparse
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import packages

ROOT=Path(__file__).resolve().parents[1]

class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        (self.root/'templates/delivery').mkdir(parents=True)
        import shutil
        shutil.copyfile(ROOT/'templates/delivery/VERIFY.py',self.root/'templates/delivery/VERIFY.py')
        self.folder=self.root/'packages/test-kit';self.folder.mkdir(parents=True)
        for name in ('source/background.png','payload/favicon.ico','payload/site.webmanifest','payload/android-res/icon.png','payload/rounded-logo/logo.png','source-assets.json'):
            p=self.folder/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(name)
        self.data=dict(version=1,id='test-kit',name='测试交付',state='approved',text='阅',theme='dark',surfaces=list(packages.SURFACES),entrypoints={x:[] for x in packages.SURFACES},approval={'user_confirmation':'测试夹具确认'},limitations=[])
        packages.write_json(self.folder/'quality-review.json',{'passed':True,'scope':'test fixture'})
        packages.documentation(self.folder,self.data,self.root);packages.finish(self.folder,self.data)
    def tearDown(self):self.tmp.cleanup()
    def test_portable_policy_links_do_not_claim_missing_repo_files_exist(self):
        note=self.folder/'source/POLICY.md'
        note.write_text('[有效](background.png) [历史](missing.md) [官方](https://example.com/doc)')
        packages.portable_source_docs(self.folder)
        text=note.read_text()
        self.assertIn('[有效](background.png)',text);self.assertIn('[官方](https://example.com/doc)',text)
        self.assertNotIn('[历史](missing.md)',text);self.assertIn('原仓库参考：missing.md',text)

    def test_exact_inventory_detects_drift_missing_and_extra(self):
        verify=packages.verifier(self.root);verify(self.folder)
        p=self.folder/'payload/favicon.ico';original=p.read_bytes();p.write_bytes(b'changed')
        with self.assertRaises(ValueError):verify(self.folder)
        p.write_bytes(original);p.unlink()
        with self.assertRaises(ValueError):verify(self.folder)
        p.write_bytes(original);extra=self.folder/'unexpected';extra.write_text('extra')
        with self.assertRaises(ValueError):verify(self.folder)
    def test_symlink_rejected_even_if_pointing_inside(self):
        (self.folder/'alias').symlink_to(self.folder/'README.md')
        with self.assertRaises(ValueError):packages.verifier(self.root)(self.folder)
    def test_web_export_has_ai_context_and_excludes_android(self):
        args=argparse.Namespace(id='test-kit',surface=['web'],mode='editable',output=self.root/'.exports/web-kit')
        result=packages.export(args,self.root);packages.verifier(self.root)(result)
        self.assertTrue((result/'quality-review.json').exists());self.assertNotIn('python3 source/scripts/visual_qa.py payload',(result/'README.md').read_text());self.assertTrue((result/'AGENTS.md').exists());self.assertTrue((result/'source/background.png').exists())
        self.assertTrue((result/'payload/favicon.ico').exists());self.assertFalse((result/'payload/android-res').exists())
        import zipfile
        with zipfile.ZipFile(result.with_suffix('.zip')) as z:
            self.assertIsNone(z.testzip());self.assertIn('web-kit/VERIFY.py',z.namelist());self.assertTrue(all(x.startswith('web-kit/') and '..' not in x.split('/') for x in z.namelist()))
        with self.assertRaises(ValueError):packages.export(args,self.root)
    def test_reject_output_outside_exports_and_unapproved_package(self):
        with self.assertRaises(ValueError):packages.export(argparse.Namespace(id='test-kit',surface=['web'],output=self.root/'outside'),self.root)
        self.data['state']='draft';packages.finish(self.folder,self.data)
        with self.assertRaises(ValueError):packages.export(argparse.Namespace(id='test-kit',surface=['web'],output=self.root/'.exports/a'),self.root)
    def test_all_export_keeps_original_artifact_files(self):
        result=packages.export(argparse.Namespace(id='test-kit',surface=['all'],mode='editable',output=self.root/'.exports/full'),self.root)
        self.assertTrue((result/'payload/android-res/icon.png').exists());self.assertTrue((result/'payload/rounded-logo/logo.png').exists())
    def test_default_install_omits_editable_material_and_preserves_web_dependencies(self):
        result=packages.export(argparse.Namespace(id='test-kit',surface=['web'],output=self.root/'.exports/install'),self.root)
        data=packages.verifier(self.root)(result)
        self.assertEqual(data['mode'],'install')
        self.assertFalse((result/'source').exists())
        self.assertTrue((result/'payload/favicon.ico').exists())
        self.assertTrue((result/'payload/site.webmanifest').exists())
        self.assertTrue((result/'source-assets.json').exists())
        self.assertTrue((result/'quality-review.json').exists())
        self.assertNotIn('python3 source/scripts/visual_qa.py payload',(result/'README.md').read_text())
        self.assertFalse((result/'payload/android-res').exists())

    def test_install_keeps_platform_resources_but_not_design_layers(self):
        for name in ('payload/macos-legacy/AppIcon.icns','payload/macos-legacy/AppIcon.iconset/icon_16x16.png','payload/macos-legacy/export.json','payload/android-adaptive/foreground-layer.png','payload/rounded-logo/preview-128.png'):
            file=self.folder/name;file.parent.mkdir(parents=True,exist_ok=True);file.write_text(name)
        packages.finish(self.folder,self.data)
        result=packages.export(argparse.Namespace(id='test-kit',surface=['macos','android'],output=self.root/'.exports/platform'),self.root)
        self.assertTrue((result/'payload/macos-legacy/AppIcon.iconset/icon_16x16.png').exists())
        self.assertTrue((result/'payload/android-res/icon.png').exists())
        self.assertFalse((result/'payload/macos-legacy/export.json').exists())
        self.assertFalse((result/'payload/android-adaptive').exists())
        self.assertFalse((result/'payload/rounded-logo').exists())
        with self.assertRaises(ValueError):
            packages.export(argparse.Namespace(id='test-kit',surface=['web'],mode='bad',output=self.root/'.exports/bad-mode'),self.root)

    def test_missing_platform_entrypoint_is_not_exported_as_complete(self):
        self.data['entrypoints']['web']=['payload/missing-icon.png']
        packages.finish(self.folder,self.data)
        out=self.root/'.exports/missing'
        with self.assertRaisesRegex(ValueError,'缺少接入入口'):
            packages.export(argparse.Namespace(id='test-kit',surface=['web'],output=out),self.root)
        self.assertFalse(out.exists());self.assertFalse(out.with_suffix('.zip').exists())

    def test_cannot_escape_package_id(self):
        for identifier in ('../elsewhere','/tmp/a','bad_ID'):
            with self.assertRaises(ValueError):packages.package_dir(self.root,identifier)
    def make_asset(self, approved):
        from library import add, create_svg, write_json
        (self.root/'catalog').mkdir();(self.root/'assets').mkdir()
        file=self.root/'icon.svg';file.write_text(create_svg('icons','阅','#123456'))
        item=add(file,'sample','已确认图例','icons',['图例'],'original','unknown','unknown','fixture',root=self.root)
        if approved:
            item['approval']={'user_confirmation':'测试夹具确认','reviewed_sha256':item['sha256']}
            write_json(self.root/'catalog/sample.json',item)
        return item
    def test_single_approved_asset_portable_delivery(self):
        item=self.make_asset(True)
        result=packages.asset(argparse.Namespace(id='sample',output=self.root/'.exports/icon'),self.root)
        data=packages.verifier(self.root)(result)
        self.assertEqual(data['type'],'single-asset');self.assertEqual(packages.sha(result/'payload/sample.svg'),item['sha256'])
        self.assertIn('没有额外生成', (result/'README.md').read_text())
    def test_unconfirmed_asset_cannot_be_exported_as_approved(self):
        self.make_asset(False)
        with self.assertRaises(ValueError):packages.asset(argparse.Namespace(id='sample',output=self.root/'.exports/icon'),self.root)

    def test_known_layout_issue_blocks_package_and_asset_reexport(self):
        notice={'block_export':True,'reason':'正文未居中','record':'docs/centering.md'}
        packages.write_json(self.root/'packages/advisories.json',{'packages':{'test-kit':notice},'assets':{'sample':notice}})
        with self.assertRaisesRegex(ValueError,'暂停新导出'):
            packages.export(argparse.Namespace(id='test-kit',surface=['all'],output=self.root/'.exports/blocked'),self.root)
        with self.assertRaisesRegex(ValueError,'暂停新导出'):
            packages.asset(argparse.Namespace(id='sample',output=self.root/'.exports/blocked'),self.root)
        packages.verifier(self.root)(self.folder)  # Historical bytes remain verifiable.
        self.assertFalse((self.root/'.exports/blocked').exists())

    def test_archive_rejects_changed_files_extra_files_and_escape(self):
        source=self.root/'.drafts/bad';source.mkdir(parents=True)
        file=source/'logo.png';file.write_bytes(b'fixture')
        args=argparse.Namespace(id='new-kit',source=source,approval='测试夹具确认')
        kit={'files':{'logo.png':'0'*64}}
        packages.write_json(source/'kit.json',kit)
        with self.assertRaisesRegex(ValueError,'文件已变化'):packages.archive(args,self.root)
        kit['files']={'../outside':'0'*64};packages.write_json(source/'kit.json',kit)
        with self.assertRaisesRegex(ValueError,'路径越界'):packages.archive(args,self.root)
        kit['files']={'logo.png':packages.sha(file)};packages.write_json(source/'kit.json',kit);(source/'extra').write_text('extra')
        with self.assertRaisesRegex(ValueError,'未登记文件'):packages.archive(args,self.root)
        self.assertFalse((self.root/'packages/new-kit').exists())

    def test_new_archive_rejects_unchecked_legacy_layout(self):
        item=self.make_asset(True)
        source=self.root/'.drafts/legacy';(source/'rounded-logo').mkdir(parents=True)
        render=source/'rounded-logo/render.json'
        packages.write_json(render,{'background_sha256':item['sha256'],'layout_version':1})
        packages.write_json(source/'kit.json',{'profiles':['rounded-logo'],'files':{'rounded-logo/render.json':packages.sha(render)}})
        args=argparse.Namespace(id='legacy-rearchive',name='测试包',source=source,approval='测试夹具确认',asset=['sample'],background_asset='sample')
        with self.assertRaisesRegex(ValueError,'layout_version=2'):packages.archive(args,self.root)
        self.assertFalse((self.root/'packages/legacy-rearchive').exists())

    def test_manifest_path_escape_is_rejected(self):
        outside=self.root/'outside';outside.write_text('x')
        self.data['files']={'../outside':{'sha256':packages.sha(outside),'bytes':1}}
        packages.write_json(self.folder/'package.json',self.data)
        with self.assertRaises(ValueError):packages.verifier(self.root)(self.folder)

class ApprovedArchiveTests(unittest.TestCase):
    def test_approved_original_bytes_and_reproduction_context(self):
        folder=ROOT/'packages/yue-surface-kit-v02'
        if not folder.exists():self.skipTest('本测试副本未包含正式交付包')
        data=packages.verifier(ROOT)(folder)
        self.assertTrue((folder/'quality-review.json').exists())
        self.assertEqual(data['state'],'approved');self.assertEqual(data['approval']['original_file_count'],185)
        for name,digest in data['approval']['original_files'].items():
            self.assertEqual(packages.sha(folder/'payload'/name),digest)
        self.assertTrue((folder/'source/scripts/render-logo.sh').exists());self.assertTrue((folder/'source/resources/fonts/mashanzheng/OFL.txt').exists())
