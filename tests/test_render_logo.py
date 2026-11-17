import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]

@unittest.skipUnless(platform.system()=='Darwin' and shutil.which('swift'),'原生渲染需 macOS/Swift')
class RenderTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.folder=Path(self.tmp.name)
        self.background=ROOT/'assets/logos/product-macrightclick-app-icon-ink-light-a-q96-v01-png.png'
    def tearDown(self): self.tmp.cleanup()
    def render(self,text,profile='circle-logo',name='out',extra=(),expected=0):
        output=self.folder/name
        result=subprocess.run([str(ROOT/'scripts/render-logo.sh'),'--background',str(self.background),'--text',text,'--profile',profile,'--theme','light','--output',str(output),*extra],capture_output=True,text=True,timeout=45)
        self.assertEqual(result.returncode,expected,result.stdout+result.stderr)
        return output
    def test_fixed_font_and_transparent_shape(self):
        output=self.render('阅'); data=json.loads((output/'render.json').read_text())
        self.assertEqual(data['font_postscript'],'MaShanZheng-Regular')
        self.assertEqual(data['seal_placement'],'right-lower')
        self.assertEqual([x['text'] for x in data['glyphs']],['阅'])
        self.assertTrue(data['all_glyph_bounds_inside_shape'])
        self.assertEqual(data['alpha_bottom_left'],0)
        self.assertEqual(data['alpha_center'],255)
    def test_main_outline_center_is_canvas_center_and_seal_independent(self):
        for profile,text,no_seal in [('circle-logo','阅',False),('rounded-logo','阅',False),('square-master','古月阅',False),('circle-logo','古月',True)]:
            output=self.render(text,profile=profile,name=profile+str(no_seal),extra=('--no-seal',) if no_seal else ())
            data=json.loads((output/'render.json').read_text())
            self.assertEqual(data['layout_version'],3)
            self.assertEqual(data['main_center_policy'],'canvas-center')
            glyphs=[x for x in data['glyphs'] if x['role']=='main']
            center_x=(min(x['x'] for x in glyphs)+max(x['x']+x['width'] for x in glyphs))/2
            center_y=(min(x['y'] for x in glyphs)+max(x['y']+x['height'] for x in glyphs))/2
            self.assertAlmostEqual(center_x,data['width']/2,delta=0.5)
            self.assertAlmostEqual(center_y,data['height']/2,delta=0.5)
            self.assertTrue(data['main_center_check_passed'])
            self.assertTrue(data['all_glyph_bounds_inside_shape'])

    def test_right_lower_seal_uses_reference_relationship_without_moving_main(self):
        for profile in ('circle-logo','rounded-logo'):
            base=self.render('阅',profile=profile,name=profile+'-base',extra=('--seal-placement','profile-default'))
            proposed=self.render('阅',profile=profile,name=profile+'-seal',extra=('--seal-placement','right-lower'))
            before=json.loads((base/'render.json').read_text());after=json.loads((proposed/'render.json').read_text())
            self.assertEqual([g for g in before['glyphs'] if g['role']=='main'],[g for g in after['glyphs'] if g['role']=='main'])
            old=before['seal_bounds'];new=after['seal_bounds']
            self.assertTrue(new['x']>old['x'] and new['y']<old['y'] and new['height']<old['height'])
            self.assertEqual(after['seal_kind'],'fixed-alpha-mask')
            self.assertAlmostEqual(new['width']/new['height'],60/111)
            self.assertEqual(after['seal_color'],'A63A30')
            self.assertTrue(after['seal_frame_inside_shape']);self.assertTrue(after['all_glyph_bounds_inside_shape'])
            self.assertEqual(after['seal_placement'],'right-lower')
        self.render('阅',profile='favicon',name='bad-seal',extra=('--seal-placement','right-lower'),expected=1)

    def test_independent_seal_is_pinned_tinted_and_embedded(self):
        import base64
        import xml.etree.ElementTree as ET
        for theme,color in [('light','A63A30'),('dark','CF6650')]:
            out=self.render('阅',name='seal-'+theme,extra=('--theme',theme))
            d=json.loads((out/'render.json').read_text())
            self.assertEqual(d['seal_sha256'],'5f36bc94e402258a98de0fccf577fbf4fb3c464e784f5c926d3e6c39ceb30f9b')
            self.assertEqual(d['seal_color'],color)
            self.assertEqual([g['role'] for g in d['glyphs']],['main'])
            self.assertEqual(hashlib.sha256((out/'seal-source.png').read_bytes()).hexdigest(),d['seal_sha256'])
            image=ET.parse(out/'foreground.svg').getroot().find('{http://www.w3.org/2000/svg}image')
            self.assertEqual(base64.b64decode(image.attrib['href'].split(',',1)[1]),(out/'seal-layer.png').read_bytes())
        self.render('阅',name='override',extra=('--seal-image','bad.png'),expected=1)

    def test_multichar_layout_and_bounds(self):
        for text,cols,rows in [('古月',2,1),('古月阅',2,2),('古月读书',2,2),('古月读书手记',3,2)]:
            output=self.render(text,name='n'+str(len(text)))
            data=json.loads((output/'render.json').read_text())
            self.assertEqual((data['layout_columns'],data['layout_rows']),(cols,rows))
            self.assertTrue(data['all_glyph_bounds_inside_shape'])
    def test_unsupported_glyph_and_long_text_rejected(self):
        self.render('🫠',expected=1)
        self.render('古'*13,expected=1)
    def test_pwa_fullbleed_and_safe_zone(self):
        output=self.render('阅',profile='pwa-maskable')
        data=json.loads((output/'render.json').read_text())
        self.assertEqual(data['alpha_bottom_left'],255)
        self.assertTrue(data['maskable_glyph_safe_zone_passed'])
    def test_no_overwrite_and_font_pin(self):
        self.render('阅'); self.render('阅',expected=1)
        provenance=json.loads((ROOT/'resources/fonts/mashanzheng/provenance.json').read_text())
        self.assertEqual(hashlib.sha256((ROOT/'resources/fonts/mashanzheng/MaShanZheng-Regular.ttf').read_bytes()).hexdigest(),provenance['sha256'])

    def test_legacy_macos_packaging_and_no_overwrite(self):
        source=self.render('阅',profile='rounded-logo')/'logo.png'
        output=self.folder/'macos'
        result=subprocess.run([str(ROOT/'scripts/export-macos.sh'),str(source),str(output)],capture_output=True,text=True,timeout=45)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual((output/'AppIcon.icns').read_bytes()[:4],b'icns')
        self.assertEqual(len(list((output/'AppIcon.iconset').glob('*.png'))),10)
        repeated=subprocess.run([str(ROOT/'scripts/export-macos.sh'),str(source),str(output)],capture_output=True,timeout=45)
        self.assertNotEqual(repeated.returncode,0)

    def test_browser_and_android_profiles(self):
        for profile,dimensions in [('favicon',(256,256)),('apple-touch',(180,180)),('og-image',(1200,630)),('android-adaptive',(1080,1080))]:
            output=self.render('阅',profile=profile,name=profile)
            data=json.loads((output/'render.json').read_text())
            self.assertEqual((data['width'],data['height']),dimensions)
            self.assertTrue((output/'foreground-layer.png').exists())
            self.assertTrue((output/'background-layer.png').exists())
            if profile=='android-adaptive':
                self.assertTrue(data['android_glyph_safe_zone_passed'])
        self.render('古月阅',profile='favicon',name='too-long-tab',expected=1)
