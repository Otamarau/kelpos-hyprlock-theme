import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("visualizer", Path(__file__).resolve().parents[1] / "lock-with-cava.py")
visualizer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visualizer)


class VisualizerTests(unittest.TestCase):
    def test_silence_and_bad_frames_are_hidden(self):
        for raw in [b"", b"oops;", b"1;2;", b"0;" * 20]:
            self.assertEqual(visualizer.render_frame(raw), "")

    def test_full_frame_produces_twenty_bars(self):
        frame = visualizer.render_frame(b"8;" * 20)
        self.assertEqual(frame.count("█"), 20)
        self.assertTrue(frame.startswith('<span letter_spacing="2048">'))
        self.assertTrue(frame.endswith("</span>"))

    def test_levels_are_clamped(self):
        frame = visualizer.render_frame(b"-4;99;" * 10)
        self.assertEqual(frame.count("█"), 10)
        self.assertEqual(frame.count("\u2007"), 10)


if __name__ == "__main__":
    unittest.main()
