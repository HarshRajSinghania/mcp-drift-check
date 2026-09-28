import re
import unittest
from pathlib import Path

import mcp_drift_check


class PackageMetadataTests(unittest.TestCase):
    def test_runtime_version_matches_pyproject(self):
        text = Path("pyproject.toml").read_text(encoding="utf-8")
        match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
        self.assertIsNotNone(match, "pyproject.toml project version not found")
        self.assertEqual(mcp_drift_check.__version__, match.group(1))


if __name__ == "__main__":
    unittest.main()
