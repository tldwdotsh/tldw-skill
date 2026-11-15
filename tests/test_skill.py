import tempfile
import unittest
from pathlib import Path
from shutil import copytree

from scripts.build import build
from scripts.validate import ROOT, validate


class SkillTests(unittest.TestCase):
    def test_hashes_and_deterministic_build(self):
        manifest, contents = validate()
        self.assertEqual(manifest["name"], "tldw")
        self.assertIn("SKILL.md", contents)
        with tempfile.TemporaryDirectory() as temp:
            first = build(Path(temp) / "a")
            second = build(Path(temp) / "b")
            self.assertEqual(first, second)

    def test_modified_resource_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "skill"
            copytree(
                ROOT,
                root,
                ignore=lambda _p, names: {n for n in names if n in {"dist", ".git", "__pycache__"}},
            )
            (root / "SKILL.md").write_text("modified")
            with self.assertRaisesRegex(ValueError, "checksum"):
                validate(root)


if __name__ == "__main__":
    unittest.main()
