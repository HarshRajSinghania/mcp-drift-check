import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".py", ".toml", ".txt"}


class RepositoryQualityTests(unittest.TestCase):
    def test_no_legacy_mcp_scan_route_in_repository_text(self):
        offenders = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES and path.name != "action.yml":
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if "orynval.com/mcp-scan" in text:
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [], f"Legacy Orynval MCP route remains in: {offenders}")

    def test_readme_uses_current_browser_route(self):
        text = README.read_text(encoding="utf-8")
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
