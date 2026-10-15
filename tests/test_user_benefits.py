from pathlib import Path
import importlib.util, unittest, tempfile, subprocess, sys, json, zipfile, io, struct, os
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

class GalleryDecode(unittest.TestCase):
    def test_corrupt_raster_rejected_before_output_created(self):
        m=load('gallery',ROOT/'scripts/build_gallery.py')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'a.png').write_bytes(b'not an image'); manifest=p/'m.json'
            manifest.write_text(json.dumps({'anchor':'a.png','variants':[{'anchor':'a.png','image':'a.png','prompt':'demo','status':'UNKNOWN'}]}))
            with self.assertRaises(ValueError): m.build(manifest,p/'out')
            self.assertFalse((p/'out').exists())

if __name__=="__main__": unittest.main()
