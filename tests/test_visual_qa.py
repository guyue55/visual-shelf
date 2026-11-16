import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from visual_qa import inspect_geometry

class VisualQATests(unittest.TestCase):
    def fixture(self):
        return {'profile':'rounded-logo','width':1024,'height':1024,'layout_version':2,'text':'阅','seal':'古月','seal_placement':'right-lower','seal_frame_inside_shape':True,'main_center_check_passed':True,'all_glyph_bounds_inside_shape':True,'seal_bounds':{'x':870,'y':280,'width':66,'height':148},'glyphs':[{'text':'阅','role':'main','x':400,'y':300,'width':224,'height':424},{'text':'古','role':'seal','x':880,'y':360,'width':40,'height':40},{'text':'月','role':'seal','x':880,'y':290,'width':40,'height':50}]}
    def test_correct_geometry(self):self.assertEqual(inspect_geometry(self.fixture()),[])
    def test_recomputes_center_instead_of_trusting_flag(self):
        d=self.fixture();d['glyphs'][0]['x']+=15
        self.assertTrue(any('未居中' in x for x in inspect_geometry(d)))
    def test_seal_text_and_overlap_are_independent_checks(self):
        d=self.fixture();d['glyphs'][1]['text']='右';d['seal_bounds']['x']=500;d['seal_bounds']['y']=400
        errors=inspect_geometry(d);self.assertIn('印章文字不准确',errors);self.assertIn('主文字与章框重叠',errors)
    def test_old_seal_policy_is_not_allowed_for_new_logo(self):
        d=self.fixture();d['seal_placement']='profile-default';self.assertTrue(any('右下' in x for x in inspect_geometry(d)))

    def test_nonfinite_coordinate_is_rejected(self):
        d=self.fixture();d['glyphs'][0]['x']=float('nan');self.assertTrue(any('非有限' in x for x in inspect_geometry(d)))
    def test_full_seal_border_is_checked_even_when_flag_is_true(self):
        d=self.fixture();d['seal_bounds']['x']=1000;self.assertIn('完整章框含描边超出形状',inspect_geometry(d))

class CurrentReferenceTests(unittest.TestCase):
    def test_templates_only_reference_current_approved_assets_and_package(self):
        import json
        root=Path(__file__).resolve().parents[1]
        styles=json.loads((root/'templates/visual/styles.json').read_text())
        records={json.loads(p.read_text())['id']:json.loads(p.read_text()) for p in (root/'catalog').rglob('*.json')}
        for style in ('ink-light-a','moonlit-blue'):
            for identifier in styles[style]['accepted_examples']:
                self.assertIn('-v04-',identifier);self.assertIn(identifier,records)
                self.assertEqual(records[identifier]['approval']['render']['seal_placement'],'right-lower')
            self.assertEqual(styles[style]['seal_placement'],'right-lower')
        self.assertEqual(styles['moonlit-blue']['delivery_packages'],['yue-surface-kit-v02'])
        self.assertTrue((root/'packages/yue-surface-kit-v02/package.json').exists())
        self.assertFalse((root/'packages/yue-surface-kit-v01').exists())
        self.assertFalse(any('-v02-png' in x and 'guyue-yue' in x for x in records))
