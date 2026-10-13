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

import yaml

from mkdocs.structure.files import File


ROOT = Path(__file__).resolve().parents[1]


def on_files(files, config):
    for source, destination in (
        ("LICENSE", "assets/legal/LICENSE.txt"),
        ("NOTICE", "assets/legal/NOTICE.txt"),
        ("THIRD_PARTY_NOTICES.md", "assets/legal/THIRD_PARTY_NOTICES.txt"),
        ("CITATION.cff", "assets/CITATION.cff"),
        (".zenodo.json", "assets/zenodo.json"),
    ):
        files.append(File.generated(config, destination, abs_src_path=str(ROOT / source)))
    return files


def on_page_markdown(markdown, page, **kwargs):
    if page.file.src_uri not in {"index.md", "references.md"}:
        return markdown
    cff = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    if page.file.src_uri == "index.md":
        badge = ""
        if cff.get("doi"):
            badge = (
                '<p class="hero__citation">'
                f'<a class="doi-badge" href="https://doi.org/{cff["doi"]}" '
                f'aria-label="Archived GFMR version {cff["version"]}, DOI {cff["doi"]}">'
                '<span class="doi-badge__label">DOI</span>'
                f'<span class="doi-badge__value">{cff["doi"]}</span></a>'
                '<a class="hero__cite-link" href="references.html#how-to-cite">How to cite →</a></p>'
            )
        return markdown.replace("<!-- GFMR_DOI_BADGE -->", badge)
    authors = [f'{author["family-names"]}, {author["given-names"][0]}.' for author in cff["authors"]]
    year = str(cff.get("date-released", "2026"))[:4]
    version = f' (Version {cff["version"]})' if cff.get("version") else ""
    citation = f'{", ".join(authors[:-1])}, & {authors[-1]} ({year}). *{cff["title"]}*{version}. Saltfoss Energy ApS. '
    if cff.get("doi"):
        doi_url = f'https://doi.org/{cff["doi"]}'
        citation += f'[{cff["doi"]}]({doi_url}).'
        status = f'Archived release: **{cff["version"]}**, published **{cff["date-released"]}**. Cite this version DOI for reproducible comparisons. Later website edits may differ from this archived release.'
    else:
        citation += f'[GFMR website]({cff["url"]}).'
        status = "A Zenodo DOI has not yet been assigned. Until a release is archived, include your access date and the repository commit used in your work. Cite the DOI for the specific version used once it is available."
    return markdown.replace("<!-- GFMR_CITATION -->", citation).replace("<!-- GFMR_DOI_STATUS -->", status)
