import re
import unittest
from pathlib import Path

import mcp_drift_check
import orynval_security_check


class PackageMetadataTests(unittest.TestCase):
    def test_runtime_versions_match_pyproject(self):
        text = Path("pyproject.toml").read_text(encoding="utf-8")
        match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
        self.assertIsNotNone(match, "pyproject.toml project version not found")
        project_version = match.group(1)
        self.assertEqual(mcp_drift_check.__version__, project_version)
        self.assertEqual(orynval_security_check.__version__, project_version)


if __name__ == "__main__":
    unittest.main()
