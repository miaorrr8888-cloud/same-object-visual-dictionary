from pathlib import Path
import importlib.util, unittest, tempfile, subprocess, sys, json, zipfile, io, os
R=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

class Gallery(unittest.TestCase):
    def fixture(self,d,**overrides):
        p=Path(d); from PIL import Image; Image.new('RGB',(8,8),'white').save(p/'a.png'); Image.new('RGB',(8,8),'black').save(p/'b.png')
        card={'anchor':'a.png','image':'b.png','prompt':'<script>bad</script>','status':'UNKNOWN'}; card.update(overrides)
        manifest=p/'manifest.json'; manifest.write_text(json.dumps({'anchor':'a.png','variants':[card]})); return manifest
    def test_gallery_escapes_prompt_and_copies(self):
        m=load('gallery',R/'scripts/build_gallery.py')
        with tempfile.TemporaryDirectory() as d:
            page=m.build(self.fixture(d),Path(d)/'out'); self.assertNotIn('<script>',page.read_text()); self.assertEqual(len(list((page.parent/'images').iterdir())),2)
    def test_mixed_anchor_rejected(self):
        m=load('gallery',R/'scripts/build_gallery.py')
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): m.build(self.fixture(d,anchor='other.png'),Path(d)/'out')
    def test_path_escape_rejected(self):
        m=load('gallery',R/'scripts/build_gallery.py')
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): m.build(self.fixture(d,image='../outside.png'),Path(d)/'out')

if __name__=="__main__": unittest.main(verbosity=2)
