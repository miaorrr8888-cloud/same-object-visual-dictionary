from pathlib import Path
import importlib.util,unittest,tempfile,json,sys,subprocess,os
ROOT=Path(__file__).resolve().parents[1]
def load(path):
    sys.path.insert(0,str(ROOT/'scripts'))
    spec=importlib.util.spec_from_file_location('extension',ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class HumanQA(unittest.TestCase):
    def setup_files(self,d):
        from PIL import Image
        p=Path(d);Image.new('RGB',(8,8),'red').save(p/'a.png');(p/'manifest.json').write_text(json.dumps({'variants':[{'image':'a.png'}]}));return p/'manifest.json'
    def test_no_review_stays_pending(self):
        with tempfile.TemporaryDirectory() as d:
            r=load('scripts/review_gallery.py').review(self.setup_files(d),{'reviews':[]});self.assertEqual(r['accepted'],0)
    def test_accept_needs_checks(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):load('scripts/review_gallery.py').review(self.setup_files(d),{'reviews':[{'image':'a.png','decision':'accept'}]})
    def test_explicit_review_binds_image_hash(self):
        with tempfile.TemporaryDirectory() as d:
            r=load('scripts/review_gallery.py').review(self.setup_files(d),{'reviews':[{'image':'a.png','decision':'accept','reviewer':'Demo reviewer','same_object':True,'text_checked':True}]})
            self.assertEqual(r['accepted'],1);self.assertEqual(len(r['variants'][0]['sha256']),64);self.assertFalse(r['variants'][0]['auto_verified'])
