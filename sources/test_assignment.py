"""Exercise the draft gate with a small two-master repository."""
from pathlib import Path
import os
import plistlib
import subprocess
import sys
import tempfile
import unittest

GATE = Path(__file__).with_name("check_assignment.py").resolve()
GREEN = "0.04,0.57,0.04,1"
PURPLE = "0.54,0.44,0.88,1"
POINT = '<point x="0" y="0" type="line"/>'


def glif(name, color, body):
    return (f'<glyph name="{name}" format="2"><advance width="500"/><outline>{body}</outline>'
            f'<lib><dict><key>public.markColor</key><string>{color}</string></dict></lib></glyph>')


class AssignmentTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        sources = self.root / "sources"
        sources.mkdir()
        (sources / "config.yaml").write_text("sources: [Test.designspace]\n")
        (self.root / "CONTEXT.md").write_text(
            '```toml\n[colors.green]\nrgba=[[0.04,0.57,0.04,1]]\n'
            '[colors.purple]\nrgba=[[0.54,0.44,0.88,1]]\n```\n')
        entries = []
        for style in ("Regular", "Black"):
            folder = sources / f"{style}.ufo/glyphs"
            folder.mkdir(parents=True)
            entries.append(f'<source stylename="{style}" filename="{style}.ufo"/>')
            contents = {}
            for name in ("leaf", "locked", "donor", "composite"):
                contents[name] = name + ".glif"
                shape = '<component base="donor"/>' if name == "composite" else f"<contour>{POINT * 3}</contour>"
                (folder / contents[name]).write_text(glif(name, GREEN if name == "locked" else PURPLE, shape))
            (folder / "contents.plist").write_bytes(plistlib.dumps(contents))
        (sources / "Test.designspace").write_text(f"<designspace><sources>{''.join(entries)}</sources></designspace>")
        for args in (["init", "-q"], ["add", "."], ["-c", "user.name=Test", "-c", "user.email=t@example.org",
                                                "-c", "commit.gpgSign=false", "commit", "-qm", "Fixture"]):
            subprocess.run(["git", *args], cwd=self.root, check=True)

    def check(self, name, message=None):
        result = subprocess.run([sys.executable, str(GATE), "--base", "HEAD", "--glyphs", name,
                                 "--masters", "Regular"], cwd=self.root, capture_output=True, text=True,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        self.assertEqual(result.returncode, int(message is not None), result.stdout + result.stderr)
        if message:
            self.assertIn(message, result.stdout)

    def glyph(self, name, style="Regular"):
        return self.root / f"sources/{style}.ufo/glyphs/{name}.glif"

    def test_scope_and_locks(self):
        for name, style, expected in (("leaf", "Regular", None), ("locked", "Regular", "protected green"),
                                      ("donor", "Regular", "component donor"), ("leaf", "Black", "Outside assignment")):
            with self.subTest(name=name, style=style):
                path = self.glyph(name, style)
                original = path.read_text()
                path.write_text(original.replace('x="0"', 'x="1"', 1).replace(GREEN, PURPLE))
                self.check(name, expected)
                path.write_text(original)
        (self.root / "unassigned.txt").touch()
        self.check("leaf", "Outside assignment")

    def test_topology_and_deletion(self):
        path = self.glyph("leaf")
        path.write_text(path.read_text().replace(POINT, "", 1))
        self.check("leaf", "topology differs")
        path.unlink()
        self.check("leaf", "cannot delete")


if __name__ == "__main__":
    unittest.main()
