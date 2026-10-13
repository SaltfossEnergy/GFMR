<!--
archive/README.md — Purpose and preparation of the GFMR website archive.

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

# Built website for Zenodo

Run `scripts/zenodo.py prepare` as described in [RELEASING.md](../RELEASING.md) to generate `gfmr-website.zip` and its SHA-256 checksum, then commit both files before tagging the release. Zenodo's native GitHub integration preserves these files inside its repository archive. The release workflow also offers them as separate GitHub downloads.

This directory holds the most recently prepared release. Earlier versions remain available in their Git tags and Zenodo records. The regular `site/` build directory remains ignored.
