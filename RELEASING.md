<!--
RELEASING.md — Maintainer workflow for citable GFMR releases archived by Zenodo.

Copyright 2026 Saltfoss Energy ApS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Releasing the GFMR reference specification

GitHub Pages hosts the current website. Zenodo preserves reviewed releases of the reference specification, including its Markdown source, figures, material definitions, licence notices, and a built website ZIP. Each archived release receives a version DOI.

## Connect Zenodo once

1. Sign in to [Zenodo](https://zenodo.org/) and [link your GitHub account](https://help.zenodo.org/docs/profile/linking-accounts/).
2. Make sure `SaltfossEnergy/GFMR` is public. An organisation owner may need to approve the Zenodo GitHub application's access; see [GitHub's integration guidance](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content).
3. In Zenodo's profile menu, select **GitHub**, click **Sync now**, and enable `SaltfossEnergy/GFMR`. Do this **before publishing the first release**. See [Zenodo's repository setup](https://help.zenodo.org/docs/github/enable-repository/).

The native integration does not need a Zenodo API token or GitHub Actions secret. Zenodo assigns the DOI after the GitHub release is published. No DOI is assumed or reserved by this repository.

## Prepare a reviewed release

Use a version such as `1.0.0` and a matching tag `v1.0.0`. The commands below are examples; choose the version and planned publication date for the release.

```sh
.venv/bin/python -m pip install -r requirements-release.txt
.venv/bin/python scripts/zenodo.py prepare --version 1.0.0 --date YYYY-MM-DD
.venv/bin/python scripts/zenodo.py check --tag v1.0.0 --archive
```

Replace `YYYY-MM-DD` with a real date. Preparation updates `CITATION.cff` and `.zenodo.json`, removes any preceding release's DOI, performs a strict site build and publication checks, and creates:

- `archive/gfmr-website.zip`: the entire built website, including legal and citation files. Extract it and open `index.html`; navigation and offline search are included.
- `archive/gfmr-website.zip.sha256`: a SHA-256 checksum of the ZIP.

The build uses the release date for reproducible timestamps. The ZIP contains the verified website, not local environment files or uncurated input documents.

If publication is delayed or the specification changes, run preparation again with the final version and date before committing and tagging. There is no DOI until the release is published and processed by Zenodo.

Review the release's content and metadata. Commit the specification changes, `CITATION.cff`, `.zenodo.json`, and **both generated archive files** before creating the tag. `archive/` is deliberately tracked: Zenodo archives the tagged repository, and extra GitHub release attachments are not included by the native integration ([upstream feature request](https://github.com/zenodo/zenodo/issues/1235)).

```sh
git add CITATION.cff .zenodo.json archive/
git commit -m "Prepare GFMR reference release 1.0.0"
git tag -a v1.0.0 -m "GFMR reference specification 1.0.0"
git push origin main
git push origin v1.0.0
```

Commit any reviewed specification changes too. Wait for **Release archive** to pass on the tag before publishing the GitHub release. This check validates the citation schema, matches the tag to both metadata files, rebuilds the website, and compares every file with the committed ZIP.

## Publish and obtain the DOI

1. On GitHub, create a release from the existing, verified tag, describe the specification changes, and publish it. A tag alone does not trigger Zenodo's release archiving.
2. The **Release archive** workflow verifies the tagged files again and attaches the website ZIP and checksum to the GitHub release.
3. Wait for Zenodo's integration to process the release. Check the Zenodo record's title, authors, version, date, Apache-2.0 licence, and files. Its repository ZIP should contain `archive/gfmr-website.zip`. See [Zenodo's release guide](https://help.zenodo.org/docs/github/archive-software/github-upload/).
4. Copy the **version DOI** for scientific citations. Keep the **concept DOI** as a general link to all releases; it resolves to the latest archived version. See [DOI versioning](https://zenodo.org/help/versioning).

Zenodo runs independently of GitHub Actions. A failed workflow cannot retract or prevent a record that Zenodo has already published, which is why the tag must pass validation first.

## Record the assigned DOI on the live website

On the development branch, run the following with the actual version DOI from Zenodo. The value below illustrates the format; it is not an assigned GFMR DOI.

```sh
.venv/bin/python scripts/zenodo.py record-doi --version 1.0.0 --doi 10.5281/zenodo.1234567
.venv/bin/python scripts/zenodo.py check
.venv/bin/mkdocs build --strict
.venv/bin/python scripts/check_site.py
```

Commit the updated `CITATION.cff` and publish the website using the existing Website workflow. Its References page automatically displays the version DOI and release date; the README links readers to that page for the current status. The record's title, authors, and licence remain sourced from the same citation file.

Keep the published release tag and its archived ZIP unchanged. The archived first release can legitimately lack its own DOI: Zenodo assigns it after archiving. The development branch records that DOI so the current website can direct readers to the preserved version. Subsequent preparation removes that DOI before archiving the next release, preventing the previous DOI from being reused.

## Maintain metadata

Edit `CITATION.cff` for authors, affiliations, optional ORCIDs, title, abstract, keywords, and licence, then run:

```sh
.venv/bin/python scripts/zenodo.py sync
.venv/bin/python scripts/zenodo.py check
```

Commit both metadata files. `.zenodo.json` explicitly describes the reference specification as a dataset, credits Thomas Sclauzero and Lubomír Bureš as creators and Saltfoss Energy ApS as rights holder, and links the website and source repository. Zenodo gives `.zenodo.json` precedence over `CITATION.cff`; GitHub uses the citation file for its citation feature ([Zenodo documentation](https://help.zenodo.org/docs/github/describe-software/zenodo-json/)). CI checks that their shared metadata agrees.

When a release needs new content, prepare a new version and publish a new tag and release. If an archive fails, inspect the error in Zenodo's GitHub integration page before trying again. For a practice run, use [Zenodo Sandbox](https://sandbox.zenodo.org/) with a separate test repository; sandbox DOIs are not production citations.
