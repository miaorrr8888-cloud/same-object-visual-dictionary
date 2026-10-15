from pathlib import Path
import importlib.util,sys,unittest,tempfile,json
ROOT=Path(__file__).resolve().parents[1]
def load(path):
    sys.path.insert(0,str(ROOT/'scripts'))
    spec=importlib.util.spec_from_file_location('third',ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class GenerationRegistry(unittest.TestCase):
    def test_record_keeps_identity_unknown(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);Image.new('RGB',(16,16),'red').save(p/'a.png');m=load('scripts/register_generation.py')
            out=m.register(p/'a.png',p/'a.png',{'prompt':'Demo','provider':'Demo provider','generated_at':'2026-10-15T00:00:00Z'},p/'out')
            row=json.loads(out.read_text())['variants'][0];self.assertFalse(row['visual_identity_verified']);self.assertEqual(row['status'],'GENERATED')
            self.assertFalse(json.loads((p/'out/generation-record.json').read_text())['record_verified'])
    def test_missing_provider_rejected(self):
        with self.assertRaises(ValueError):load('scripts/register_generation.py').register('a','b',{'prompt':'Demo'},'not-created')
