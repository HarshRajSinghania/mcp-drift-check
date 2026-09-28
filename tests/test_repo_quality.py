import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


class RepositoryQualityTests(unittest.TestCase):
    def test_readme_has_no_legacy_mcp_scan_route(self):
        text = README.read_text(encoding="utf-8")
        self.assertNotIn("orynval.com/mcp-scan", text)
        self.assertIn("orynval.com/mcp-drift-check", text)

    def test_readme_relative_links_exist(self):
        text = README.read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
        missing = []
        for target in links:
            target = target.strip().split()[0]
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = target.split("#", 1)[0]
            if path and not (ROOT / path).exists():
                missing.append(target)
        self.assertEqual(missing, [], f"Broken relative README links: {missing}")


if __name__ == "__main__":
    unittest.main()
