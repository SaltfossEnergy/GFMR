<!--
README.md — Project documentation for the GFMR reference website.

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

# GFMR reference website

A Markdown-based publication of the **Generic FUNaK-Fuelled Thermal Molten Salt Reactor (GFMR)** reference specification, owned by Saltfoss Energy ApS.

The [website](https://SaltfossEnergy.github.io/GFMR/) is the GFMR reference. It provides the model geometry, design parameters, channel hydraulics, core lifetime criterion, and material definitions. Reference benchmark results will be added later.

## Provenance and citation

Initially developed during the master thesis work by Thomas Sclauzero at Saltfoss Energy ApS under the supervision and guidance of Lubomír Bureš. Both are credited as authors in [CITATION.cff](CITATION.cff) and on the [citation page](https://SaltfossEnergy.github.io/GFMR/references.html).

© 2026 Saltfoss Energy ApS.

## Licences

The repository and website are licensed under the [Apache License, Version 2.0](LICENSE). This covers the GFMR reference specification, website text, material-property tables, original figures, website implementation, scripts, configuration, and OpenMC code snippets. Copyright and attribution are recorded in [NOTICE](NOTICE).

Third-party components retain their own licences; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). The [website licence page](docs/licenses.md) describes the scope and attribution.

Original Markdown documentation, implementation, and configuration files carry the Apache 2.0 copyright and licence declaration. The website build includes copies of `LICENSE`, `NOTICE`, third-party notices, and `CITATION.cff`, so the published or downloaded website carries its licence and citation metadata too.

**IMPORTANT:** This model describes a generic reference design. It is NOT the proprietary Saltfoss reactor design. It is provided as a benchmark and educational tool for the broader nuclear engineering community.

See [Disclaimer & intended use](https://SaltfossEnergy.github.io/GFMR/disclaimer.html) for the full disclaimer.

## Local development

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/mkdocs build --strict
.venv/bin/python scripts/check_site.py
./scripts/preview.sh
```

## Archiving a citable version

See the [citation page](https://SaltfossEnergy.github.io/GFMR/references.html) for the current DOI status. The repository is prepared for Zenodo's GitHub integration, with explicit author and licence metadata in [`.zenodo.json`](.zenodo.json), citation metadata in [`CITATION.cff`](CITATION.cff), and release validation in GitHub Actions.

Follow [RELEASING.md](RELEASING.md) to connect Zenodo, prepare the release, and record its DOI. The preparation command builds and verifies the website and creates `archive/gfmr-website.zip`. Commit that ZIP before tagging so the built website is preserved inside Zenodo's source archive. The release workflow also attaches it to the GitHub release for convenient download.

The website's citation and DOI status are generated from `CITATION.cff`. Use the version DOI when comparing results against a particular specification; see Zenodo's [DOI versioning guidance](https://zenodo.org/help/versioning). Publishing the website alone does not assign a DOI.

