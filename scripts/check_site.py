# scripts/check_site.py — Validate the built GFMR reference website.
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

"""Check publication boundaries, intended-use links, citation, and local links.

Run after `mkdocs build --strict`. Uses only the Python standard library.
"""

from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
SITE_PREFIX = urlsplit(re.search(r"^site_url:\s*(.+)$", (ROOT / "mkdocs.yml").read_text(), re.MULTILINE)[1]).path


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.text = []
        self.links = []
        self.ids = set()
        self.ignored = 0
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style"}:
            self.ignored += 1
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag in {"img", "script"} and attrs.get("src"):
            self.links.append(attrs["src"])
        if tag == "link" and attrs.get("rel") in {"stylesheet", "icon", "preload"}:
            self.links.append(attrs["href"])

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.ignored -= 1

    def handle_data(self, data):
        if not self.ignored:
            self.text.append(data)


def normalize(text):
    return " ".join(text.split())


def main():
    assert (SITE / "index.html").is_file(), "Build the site first."
    documents = {
        path: Document(path.read_text(encoding="utf-8"))
        for path in SITE.rglob("*.html")
    }
    source = (ROOT / "Generic FUNaK-Fuelled Thermal Molten Salt Reactor (GFMR) Model.txt").read_text(encoding="utf-8-sig")
    disclaimer = normalize(source.split("DISCLAIMER:", 1)[1])
    notice = normalize(next(line for line in source.splitlines() if line.startswith("IMPORTANT:")))

    for path, doc in documents.items():
        body = normalize(" ".join(doc.text))
        assert "© 2026 Saltfoss Energy ApS" in body, f"Copyright missing: {path.name}"
        assert any(urlsplit(link).path.endswith("disclaimer.html") for link in doc.links), f"Intended-use link missing: {path.name}"
        assert any(urlsplit(link).path.endswith("licenses.html") for link in doc.links), f"Licence link missing: {path.name}"
        assert "Sources: supplied" not in body and "Source: GFMR reference" not in body, f"Obsolete source footer: {path.name}"
        assert "attached PDF document" not in body, f"Obsolete PDF claim: {path.name}"
        if path.name != "disclaimer.html":
            assert disclaimer not in body, f"Repeated full disclaimer: {path.name}"
        for link in doc.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                continue
            link_path = unquote(parts.path)
            if link_path.startswith(SITE_PREFIX):
                target = (SITE / link_path.removeprefix(SITE_PREFIX)).resolve()
            else:
                target = (path.parent / link_path).resolve() if link_path else path
            assert target.is_relative_to(SITE.resolve()), f"Link leaves site: {link}"
            if target.is_dir():
                target /= "index.html"
            assert target.exists(), f"Broken local link in {path.name}: {link}"
            if parts.fragment and target in documents:
                assert unquote(parts.fragment) in documents[target].ids, f"Broken anchor in {path.name}: {link}"

    intended_use = normalize(" ".join(documents[SITE / "disclaimer.html"].text))
    assert intended_use.count(disclaimer) == 1, "Full original disclaimer must appear once on its dedicated page."
    assert intended_use.count(notice) == 1, "Original model notice missing or repeated on its dedicated page."
    home = normalize(" ".join(documents[SITE / "index.html"].text))
    assert home.count(notice) == 1, "Original homepage model notice missing or repeated."

    overview = normalize(" ".join(documents[SITE / "overview.html"].text))
    for line in source.splitlines():
        line = normalize(line.removeprefix("* "))
        if line and not line.startswith(("IMPORTANT:", "DISCLAIMER:", "The model is described in detail")):
            assert line in overview, f"Model feature missing from overview: {line}"
    assert "under the supervision and guidance of Lubomír Bureš" in overview, "Model provenance missing."
    assert "Reference results will be added" in overview, "Benchmark status missing."
    assert (ROOT / "CITATION.cff").is_file(), "Citation metadata missing."
    assert (ROOT / "LICENSE").is_file() and (ROOT / "NOTICE").is_file(), "Repository licence or attribution notice missing."
    references = normalize(" ".join(documents[SITE / "references.html"].text))
    assert "This website is the GFMR reference specification." in references, "Website citation missing."
    metadata = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    citation_source = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    doi = re.search(r'^doi:\s*[\"\']?([^\s\"\']+)', citation_source, re.MULTILINE)
    if doi:
        assert doi[1] in references, "Assigned version DOI missing from citation page."
        assert f"https://doi.org/{doi[1]}" in documents[SITE / "references.html"].links, "Version DOI link missing."
        assert f"https://doi.org/{doi[1]}" in documents[SITE / "index.html"].links, "Homepage DOI badge missing."
        assert metadata["version"] in references, "Release version missing from citation page."
        assert "A Zenodo DOI has not yet been assigned." not in references, "Outdated DOI status."
    else:
        assert "A Zenodo DOI has not yet been assigned." in references, "DOI status missing."
        assert 'class="doi-badge"' not in (SITE / "index.html").read_text(encoding="utf-8"), "Homepage shows an unassigned DOI."

    for original, published in (
        ("LICENSE", "assets/legal/LICENSE.txt"),
        ("NOTICE", "assets/legal/NOTICE.txt"),
        ("THIRD_PARTY_NOTICES.md", "assets/legal/THIRD_PARTY_NOTICES.txt"),
        ("CITATION.cff", "assets/CITATION.cff"),
        (".zenodo.json", "assets/zenodo.json"),
    ):
        assert (ROOT / original).read_bytes() == (SITE / published).read_bytes(), f"Publication metadata missing or outdated: {published}"

    materials = documents[SITE / "materials.html"]
    assert {"funak", "graphite", "hafnium", "hastelloy-n", "helium"} <= materials.ids, "Material sections missing."
    assert "material-properties" not in materials.ids and "openmc-definition" not in materials.ids, "Repeated material subheadings remain."

    forbidden = ("fuel cycle", "online refuelling", "daily additions", "redox control", "fission product removal", "salt bubbling", "salt spraying")
    for path in SITE.rglob("*"):
        assert path.suffix.lower() != ".pdf", f"Uncurated PDF included: {path}"
        if path.suffix in {".html", ".json", ".js", ".xml", ".txt"}:
            contents = normalize(path.read_text(encoding="utf-8")).lower()
            for phrase in forbidden:
                assert phrase not in contents, f"Excluded content found in {path}: {phrase}"

    for original, published in (
        ("geometry_xy.png", "geometry-xy.png"),
        ("geometry_xz (3).png", "geometry-xz.png"),
        ("cr_hexl.png", "control-rod.png"),
    ):
        assert (ROOT / original).read_bytes() == (SITE / "assets/images" / published).read_bytes(), f"Original figure changed: {original}"

    print(f"PASS: {len(documents)} pages; local links and anchors; model features and provenance; dedicated disclaimer; Saltfoss copyright; citation and benchmark status; material sections; original figures unchanged; publication boundaries.")


if __name__ == "__main__":
    main()
