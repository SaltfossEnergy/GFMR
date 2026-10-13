# tests/test_zenodo.py — Exercise GFMR release packaging and DOI updates locally.
#
# Copyright 2026 Saltfoss Energy ApS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]


class ZenodoReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = tempfile.TemporaryDirectory(prefix="gfmr-release-tests-")
        cls.addClassCleanup(cls.workspace.cleanup)
        cls.baseline = Path(cls.workspace.name) / "baseline"
        cls.baseline.mkdir()
        for directory in ("docs", "includes", "overrides", "hooks", "scripts", "archive"):
            shutil.copytree(ROOT / directory, cls.baseline / directory, ignore=shutil.ignore_patterns("__pycache__"))
        for filename in (
            "mkdocs.yml", "LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md", "CITATION.cff", ".zenodo.json",
            "Generic FUNaK-Fuelled Thermal Molten Salt Reactor (GFMR) Model.txt",
            "geometry_xy.png", "geometry_xz (3).png", "cr_hexl.png",
        ):
            shutil.copy2(ROOT / filename, cls.baseline / filename)
        result = subprocess.run(
            [sys.executable, "scripts/zenodo.py", "prepare", "--version", "9.8.7", "--date", "2026-01-01"],
            cwd=cls.baseline, capture_output=True, text=True,
        )
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)

    def setUp(self):
        directory = tempfile.TemporaryDirectory(dir=self.workspace.name)
        self.addCleanup(directory.cleanup)
        self.checkout = Path(directory.name) / "repo"
        shutil.copytree(self.baseline, self.checkout)

    def run_command(self, *arguments, expected=0):
        result = subprocess.run(
            [sys.executable, *arguments], cwd=self.checkout, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_complete_reproducible_archive(self):
        archive = self.checkout / "archive/gfmr-website.zip"
        original = archive.read_bytes()
        with ZipFile(archive) as package:
            for name in ("index.html", "assets/legal/LICENSE.txt", "assets/legal/NOTICE.txt", "assets/CITATION.cff", "assets/zenodo.json"):
                self.assertIn(name, package.namelist())
        self.run_command("scripts/zenodo.py", "check", "--tag", "v9.8.7", "--archive")
        self.run_command("scripts/zenodo.py", "prepare", "--version", "9.8.7", "--date", "2026-01-01")
        self.assertEqual(archive.read_bytes(), original)

    def test_stale_archive_and_checksum_are_rejected(self):
        checksum = self.checkout / "archive/gfmr-website.zip.sha256"
        original = checksum.read_text()
        checksum.write_text("invalid checksum\n")
        result = self.run_command("scripts/zenodo.py", "check", "--tag", "v9.8.7", "--archive", expected=1)
        self.assertIn("checksum differs", result.stderr)
        checksum.write_text(original)
        page = self.checkout / "docs/parameters.md"
        page.write_text(page.read_text() + "\nUpdated reference parameters.\n")
        result = self.run_command("scripts/zenodo.py", "check", "--tag", "v9.8.7", "--archive", expected=1)
        self.assertIn("archive differs", result.stderr)

    def test_invalid_inputs_and_metadata_drift_are_rejected(self):
        original = (self.checkout / "CITATION.cff").read_bytes()
        self.run_command("scripts/zenodo.py", "check", "--tag", "v9.8.8", expected=1)
        self.run_command("scripts/zenodo.py", "prepare", "--version", "v9.8.7", "--date", "2026-01-01", expected=1)
        self.run_command("scripts/zenodo.py", "prepare", "--version", "9.8.7", "--date", "2026-02-30", expected=1)
        self.assertEqual((self.checkout / "CITATION.cff").read_bytes(), original)
        path = self.checkout / ".zenodo.json"
        metadata = json.loads(path.read_text())
        metadata["creators"][0]["name"] = "Incorrect author"
        path.write_text(json.dumps(metadata))
        self.run_command("scripts/zenodo.py", "check", expected=1)
        self.run_command("scripts/zenodo.py", "sync")

    def test_doi_is_rendered_and_cleared_for_the_next_release(self):
        self.run_command("scripts/zenodo.py", "record-doi", "--version", "9.8.7", "--doi", "10.5072/zenodo.1234567", expected=1)
        self.run_command("scripts/zenodo.py", "record-doi", "--version", "9.8.8", "--doi", "10.5281/zenodo.1234567", expected=1)
        self.run_command("scripts/zenodo.py", "record-doi", "--version", "9.8.7", "--doi", "10.5281/zenodo.1234567")
        self.run_command("-m", "mkdocs", "build", "--strict")
        self.run_command("scripts/check_site.py")
        page = (self.checkout / "site/references.html").read_text()
        self.assertIn("https://doi.org/10.5281/zenodo.1234567", page)
        self.assertNotIn("A Zenodo DOI has not yet been assigned.", page)
        self.run_command("scripts/zenodo.py", "prepare", "--version", "9.8.8", "--date", "2026-01-02")
        self.assertNotIn("\ndoi:", (self.checkout / "CITATION.cff").read_text())
        self.assertNotIn("doi", json.loads((self.checkout / ".zenodo.json").read_text()))


if __name__ == "__main__":
    unittest.main()
