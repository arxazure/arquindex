import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('subtitles', Path(__file__).resolve().parents[1] / 'scripts/generate-subtitles.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class SubtitlesTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'pt.srt'

    def test_structure_utf8_and_times(self):
        module.write_srt([{'start': 0, 'end': 1.234, 'text': ' Organização e segurança. '},
                          {'start': 1.234, 'end': 3, 'text': 'Ação\nArquindex'}], self.path)
        self.assertEqual(self.path.read_bytes(), ('1\n00:00:00,000 --> 00:00:01,234\nOrganização e segurança.\n\n'
            '2\n00:00:01,234 --> 00:00:03,000\nAção Arquindex\n\n').encode('utf-8'))
        self.assertEqual(module.stamp(3661.9996), '01:01:02,000')

    def test_invalid_times_text_and_overlap(self):
        for start, end in [(-1, 2), (2, 1), (1, 1), (0, float('nan')), (0, float('inf')), (0, .0001), (True, 2)]:
            with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                module.write_srt([{'start': start, 'end': end, 'text': 'x'}], self.path)
        for segments in [[], [{'start': 0, 'end': 1, 'text': ' '}],
                         [{'start': 0, 'end': 1, 'text': '-->'}],
                         [{'start': 0, 'end': 2, 'text': 'a'}, {'start': 1, 'end': 3, 'text': 'b'}]]:
            with self.assertRaises(ValueError):
                module.write_srt(segments, self.path)
        self.assertFalse(self.path.exists())

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg required')
    def test_ffmpeg_demux_mux_and_burn(self):
        module.write_srt([{'start': 0, 'end': .8, 'text': 'Digitalização: ação e segurança'}], self.path)
        data = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_packets', '-of', 'json', str(self.path)]))
        self.assertEqual(len(data['packets']), 1)
        self.assertAlmostEqual(float(data['packets'][0]['duration_time']), .8)
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(self.path), '-c:s', 'mov_text', str(self.path.with_suffix('.mp4'))], check=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'color=s=320x240:d=1',
                        '-vf', f'subtitles={self.path}', '-f', 'null', '-'], check=True)

if __name__ == '__main__':
    unittest.main()
