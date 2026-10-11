# GFMR reference website

A Markdown-based publication of the **Generic FUNaK-Fuelled Thermal Molten Salt Reactor (GFMR)** reference specification, owned by Saltfoss Energy ApS.

The [website](https://SaltfossEnergy.github.io/GFMR/) is the GFMR reference. It provides the model geometry, design parameters, channel hydraulics, core lifetime criterion, and material definitions. Reference benchmark results will be added later.

## Provenance and citation

Initially developed during the master thesis work by Thomas Sclauzero at Saltfoss Energy ApS under the supervision and guidance of Lubomír Bureš. Both are credited as authors in [CITATION.cff](CITATION.cff) and on the [citation page](https://SaltfossEnergy.github.io/GFMR/references.html).

© 2026 Saltfoss Energy ApS.

## Licences

The repository and website are licensed under the [Apache License, Version 2.0](LICENSE). This covers the GFMR reference specification, website text, material-property tables, original figures, website implementation, scripts, configuration, and OpenMC code snippets. Copyright and attribution are recorded in [NOTICE](NOTICE).

Third-party components retain their own licences; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). The [website licence page](docs/licenses.md) describes the scope and attribution.

Original implementation and configuration files carry the Apache 2.0 copyright and licence declaration. The website build includes copies of `LICENSE`, `NOTICE`, third-party notices, and `CITATION.cff`, so the published or downloaded website carries its licence and citation metadata too.

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
A Zenodo DOI has not yet been assigned. For the first archive:

1. Review the reference specification and choose a release version.
2. Connect the repository to Zenodo, using its [GitHub archiving instructions](https://help.zenodo.org/docs/github/archive-software/github-upload/), or upload a versioned archive containing the specification and built website.
3. Include Thomas Sclauzero and Lubomír Bureš as authors and Saltfoss Energy ApS as the owner/publisher.
4. Add the assigned version DOI, release version, and release date to `CITATION.cff`; update `docs/references.md` to match. Use the version DOI when comparing results against that specification.

See Zenodo's [DOI versioning guidance](https://zenodo.org/help/versioning). Publishing the website alone does not assign a DOI.

