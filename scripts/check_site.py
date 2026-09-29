"""Check the publication boundaries, original notice wording, and local links.

Run after `mkdocs build --strict`. Uses only the Python standard library.
"""

from html.parser import HTMLParser
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
        assert disclaimer in body, f"Full original disclaimer missing: {path.name}"
        assert notice in body, f"Original model notice missing: {path.name}"
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

    overview = normalize(" ".join(documents[SITE / "overview.html"].text))
    for line in source.splitlines():
        line = normalize(line.removeprefix("* "))
        if line:
            assert line in overview, f"Supplied text missing from overview: {line}"

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

    print(f"PASS: {len(documents)} pages; all local links and anchors; full supplied text; exact disclaimer and notice on every page; original figures unchanged; excluded section absent from pages, search, and assets.")


if __name__ == "__main__":
    main()
