# hooks/publication.py — Bundle GFMR publication metadata with the website.
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

"""Publish the repository's licence, attribution, and citation files with the site."""

from pathlib import Path

from mkdocs.structure.files import File


ROOT = Path(__file__).resolve().parents[1]


def on_files(files, config):
    for source, destination in (
        ("LICENSE", "assets/legal/LICENSE.txt"),
        ("NOTICE", "assets/legal/NOTICE.txt"),
        ("THIRD_PARTY_NOTICES.md", "assets/legal/THIRD_PARTY_NOTICES.txt"),
        ("CITATION.cff", "assets/CITATION.cff"),
    ):
        files.append(File.generated(config, destination, abs_src_path=str(ROOT / source)))
    return files
