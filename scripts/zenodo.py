# scripts/zenodo.py — Prepare and verify citable GFMR releases for Zenodo.
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

"""Prepare local release files; never create tags, releases, or Zenodo records."""

import argparse
from datetime import date, datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import yaml


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive/gfmr-website.zip"
VERSION = r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
DOI = r"10\.5281/zenodo\.[1-9]\d*"


def citation():
    return yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))


def metadata(cff):
    result = {
        "title": cff["title"],
        "description": cff["abstract"].strip(),
        "upload_type": cff["type"],
        "creators": [
            {
                "name": f'{author["family-names"]}, {author["given-names"]}',
                "affiliation": author["affiliation"],
                **({"orcid": author["orcid"].removeprefix("https://orcid.org/")} if "orcid" in author else {}),
            }
            for author in cff["authors"]
        ],
        "contributors": [{"name": "Saltfoss Energy ApS", "type": "RightsHolder"}],
        "license": cff["license"],
        "access_right": "open",
        "language": "eng",
        "keywords": cff["keywords"],
        "related_identifiers": [
            {"identifier": cff["url"], "relation": "isDocumentedBy", "scheme": "url"},
            {"identifier": cff["repository-code"], "relation": "isDerivedFrom", "scheme": "url"},
        ],
    }
    if cff.get("version"):
        result["version"] = str(cff["version"])
        result["publication_date"] = str(cff["date-released"])
    # Zenodo assigns a fresh DOI to each release. Never reuse the previous DOI here.
    return result


def write_metadata():
    (ROOT / ".zenodo.json").write_text(
        json.dumps(metadata(citation()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def update_citation(fields, remove=()):
    path = ROOT / "CITATION.cff"
    source = path.read_text(encoding="utf-8")
    for key in (*remove, *fields):
        source = re.sub(rf"^{re.escape(key)}:.*\n?", "", source, flags=re.MULTILINE)
    source = source.rstrip() + "\n"
    for key, value in fields.items():
        source += f"{key}: {json.dumps(value, ensure_ascii=False)}\n"
    path.write_text(source, encoding="utf-8")
    write_metadata()


def verify(tag=None):
    from cffconvert import Citation

    Citation((ROOT / "CITATION.cff").read_text(encoding="utf-8")).validate()
    cff = citation()
    actual = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    if actual != metadata(cff):
        raise ValueError(".zenodo.json differs from CITATION.cff; run the sync command.")
    if bool(cff.get("version")) != bool(cff.get("date-released")):
        raise ValueError("Set both version and date-released when preparing a release.")
    if cff.get("version"):
        if not re.fullmatch(VERSION, str(cff["version"])):
            raise ValueError("Use a release version such as 1.0.0.")
        date.fromisoformat(str(cff["date-released"]))
    if cff.get("doi"):
        if not cff.get("version") or not re.fullmatch(DOI, cff["doi"]):
            raise ValueError("A production Zenodo version DOI requires a release version.")
    if tag is not None and tag != f'v{cff.get("version", "")}':
        raise ValueError("Release tag must match CITATION.cff, e.g. v1.0.0; prepare the release first.")
    return cff


def build(cff):
    env = os.environ.copy()
    if cff.get("date-released"):
        release_date = date.fromisoformat(str(cff["date-released"]))
        env["SOURCE_DATE_EPOCH"] = str(int(datetime.combine(release_date, datetime.min.time(), timezone.utc).timestamp()))
    subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict"], cwd=ROOT, env=env, check=True)
    subprocess.run([sys.executable, "scripts/check_site.py"], cwd=ROOT, check=True)


def site_contents():
    return {
        path.relative_to(ROOT / "site").as_posix(): path.read_bytes()
        for path in sorted((ROOT / "site").rglob("*")) if path.is_file()
    }


def package():
    ARCHIVE.parent.mkdir(exist_ok=True)
    with ZipFile(ARCHIVE, "w", compression=ZIP_DEFLATED) as archive:
        for name, content in site_contents().items():
            entry = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, content)
    checksum = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    ARCHIVE.with_suffix(".zip.sha256").write_text(f"{checksum}  {ARCHIVE.name}\n", encoding="utf-8")


def verify_archive():
    if not ARCHIVE.is_file():
        raise ValueError("Website archive missing; run prepare and commit archive/gfmr-website.zip before tagging.")
    with ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        archived = {name: archive.read(name) for name in names}
        built = site_contents()
        if len(names) != len(set(names)) or archived != built:
            changed = sorted(name for name in archived.keys() | built.keys() if archived.get(name) != built.get(name))
            raise ValueError(f"Website archive differs from the verified build ({', '.join(changed[:5])}); run prepare again before tagging.")
    expected = f"{hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()}  {ARCHIVE.name}\n"
    if ARCHIVE.with_suffix(".zip.sha256").read_text(encoding="utf-8") != expected:
        raise ValueError("Website archive checksum differs; run prepare again.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("sync", help="Regenerate .zenodo.json from CITATION.cff.")
    check = commands.add_parser("check", help="Validate citation metadata and optionally the release archive.")
    check.add_argument("--tag")
    check.add_argument("--archive", action="store_true", help="Rebuild and compare the committed website ZIP.")
    prepare = commands.add_parser("prepare", help="Set release metadata, build, check, and package the website.")
    prepare.add_argument("--version", required=True, help="Version without the v prefix, e.g. 1.0.0.")
    prepare.add_argument("--date", required=True, help="Planned publication date in YYYY-MM-DD format.")
    record = commands.add_parser("record-doi", help="Record an assigned version DOI on the development branch.")
    record.add_argument("--version", required=True)
    record.add_argument("--doi", required=True, help="Assigned DOI, without https://doi.org/.")
    args = parser.parse_args()
    try:
        if args.command == "sync":
            write_metadata()
            verify()
        elif args.command == "prepare":
            if not re.fullmatch(VERSION, args.version):
                raise ValueError("Use a version such as 1.0.0, without a v prefix.")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
                raise ValueError("Use a date in YYYY-MM-DD format.")
            date.fromisoformat(args.date)
            # A new release must not claim the preceding release's DOI.
            update_citation({"version": args.version, "date-released": args.date}, remove=("doi",))
            cff = verify(f"v{args.version}")
            build(cff)
            package()
            verify_archive()
            print("Prepared release files. Review and commit CITATION.cff, .zenodo.json, and archive/ before tagging.")
        elif args.command == "record-doi":
            verify(f"v{args.version}")
            if not re.fullmatch(DOI, args.doi):
                raise ValueError("Use the assigned production Zenodo version DOI, e.g. 10.5281/zenodo.1234567.")
            update_citation({"doi": args.doi})
            verify()
            print("DOI recorded. Rebuild the live website; keep the published release tag unchanged.")
        else:
            cff = verify(args.tag)
            if args.archive:
                if not cff.get("version"):
                    raise ValueError("Prepare a release version before checking its archive.")
                build(cff)
                verify_archive()
        print("PASS: citation and Zenodo metadata" + ("; verified website archive" if getattr(args, "archive", False) else ""))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"ERROR: {error}\n")


if __name__ == "__main__":
    main()
