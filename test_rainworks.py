"""Tests for Rainworks (index.html).

Static checks always run. When Node.js is installed, the puzzle logic (the <script id="logic">
block, which has no DOM or three.js) also runs: every level must be generated the same way twice,
be a spanning tree of channels, start unsolved, be solved by its par number of turns, and be
finished by following the hints alone.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "index.html"), encoding="utf-8") as f:
    HTML = f.read()
LOGIC = re.search(r'<script id="logic">(.*?)</script>', HTML, re.S).group(1)
MODULE = re.search(r'<script type="module">(.*?)</script>', HTML, re.S).group(1)

HARNESS = """
;(function(){
  const problems=selfTestLogic();
  console.log(JSON.stringify({levels:LEVELS,problems:problems.slice(0,25)}));
  process.exitCode=problems.length?1:0;
})();
"""


def function_body(name):
    """The source of `function name(...){...}` in the module script, matched by braces."""
    start = MODULE.index("function " + name + "(")
    depth, i = 0, MODULE.index("{", start)
    while True:
        depth += {"{": 1, "}": -1}.get(MODULE[i], 0)
        if depth == 0:
            return MODULE[start:i + 1]
        i += 1


class Static(unittest.TestCase):
    def test_versions_are_pinned(self):
        imports = json.loads(re.search(r'<script type="importmap">(.*?)</script>', HTML, re.S).group(1))["imports"]
        for url in imports.values():
            self.assertRegex(url, r"three@\d+\.\d+\.\d+/")
        for url in re.findall(r'import\("(https://[^"]+)"\)', MODULE):
            self.assertRegex(url, r"@\d+\.\d+\.\d+$")

    def test_hands_first(self):
        self.assertIn('optionalFeatures:["hand-tracking"]', MODULE)
        self.assertIn('addEventListener("select"', MODULE)
        self.assertIn('"index-finger-tip"', MODULE)

    def test_logic_is_separate(self):
        self.assertNotIn("THREE", LOGIC)
        self.assertNotIn("document", LOGIC)
        self.assertIn("selfTestLogic", MODULE)

    def test_levels_table(self):
        sizes = json.loads(re.search(r"SIZES=(\[[\d,]+\])", LOGIC).group(1))
        scramble = json.loads(re.search(r"SCRAMBLE=(\[[\d,]+\])", LOGIC).group(1))
        levels = int(re.search(r"LEVELS=(\d+)", LOGIC).group(1))
        self.assertEqual(len(sizes), levels)
        self.assertEqual(sizes, sorted(sizes))
        self.assertEqual(len(scramble), levels)
        # the first island is a gentle tutorial
        self.assertGreater(scramble[0], 0)
        self.assertLessEqual(scramble[0], 3)

    def test_tutorial_and_hint(self):
        self.assertIn("function hintTile", LOGIC)
        self.assertIn('["hint","💡 Hint"]', MODULE)
        self.assertIn('$("b-hint")', MODULE)
        self.assertIn('id="b-hint"', HTML)

    def test_disclosure_and_wording(self):
        self.assertIn("Made by MV2 of Munim, Inc. with AI agents", HTML)
        self.assertIsNone(re.search(r"MV2[^.]{0,60}\b(an AI|a bot|AI assistant)\b", HTML))

    # v0.2.1: fixes from the first desktop playtest

    def test_emulator_is_forced_in(self):
        # Chrome's own navigator.xr makes IWER skip installing itself unless forced
        self.assertRegex(MODULE, r"\.installRuntime\(\{\s*forceInstall:\s*true\s*\}\)")
        self.assertNotRegex(MODULE, r"\.installRuntime\(\)")

    def test_audio_starts_only_from_a_gesture(self):
        # activate() is also called by the self-test, so it must not start audio
        self.assertNotIn("sound.unlock", function_body("activate"))
        self.assertIn("sound.unlock", function_body("poke"))
        self.assertRegex(MODULE, r'addEventListener\("pointerdown",[^\n]*sound\.unlock\(\)')
        self.assertRegex(MODULE, r'addEventListener\("select",[^\n]*sound\.unlock\(\)')
        self.assertIn("sound.started()", MODULE)

    def test_no_deprecated_clock(self):
        self.assertIsNone(re.search(r"\bTHREE\.Clock\b", MODULE))

    def test_panel_clears_the_cloud(self):
        cloud_y = float(re.search(r"CLOUD_Y=([\d.]+)", MODULE).group(1))
        panel_y = float(re.search(r"PANEL_Y=([\d.]+)", MODULE).group(1))
        self.assertGreater(panel_y, cloud_y + 0.05)
        self.assertRegex(MODULE, r"panelMesh\.position\.set\(0,PANEL_Y,")

    def test_stars_drawn_apart_from_the_headline(self):
        body = function_body("drawPanel")
        self.assertIn('g.textAlign="right"', body)
        self.assertIn("fillText(s,", body)


@unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
class Logic(unittest.TestCase):
    def test_every_level(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "rainworks_logic.js")
            with open(path, "w", encoding="utf-8") as f:
                f.write(LOGIC + "\n" + HARNESS)
            out = subprocess.run(["node", path], capture_output=True, text=True, encoding="utf-8", timeout=120)
        self.assertEqual(out.returncode, 0, out.stdout[-4000:] + out.stderr[-4000:])
        report = json.loads(out.stdout[out.stdout.index("{"):])
        self.assertEqual(report["problems"], [])


if __name__ == "__main__":
    unittest.main()
