---
title: Model overview
eyebrow: MODEL / OVERVIEW
---

<!--
docs/overview.md — Overview and provenance of the GFMR reference model.

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

# Model overview

Generic FUNaK-Fuelled Thermal Molten Salt Reactor (GFMR) Model
{ .lead }

## Overview

This repository provides the design and geometrical specifications for a Generic FUNaK-Fuelled Thermal Molten Salt Reactor (GFMR). The GFMR is intended as a reference problem for the modeling and simulation of molten salt reactors, capturing many of the essential physical phenomena relevant to graphite-moderated MSR systems.

The model specification is published on this website: [design parameters](parameters.md), [channel hydraulics](hydraulics.md), [core lifetime](lifetime.md), [geometry](geometry.md), and [materials](materials.md). It is designed to be software-agnostic and can be implemented using a single-physics approach or within a complex multiphysics framework.

## Key Model Features

* **Fuel & Moderator:** Utilizes FUNaK fuel salt with graphite moderation.
* **Thermal Power:** 150 MW.
* **Core Geometry:** A reactor height of 360 cm and a reflector diameter of 350 cm, featuring 379 fuel channels arranged in a hexagonal lattice.
* **Zoned Velocity:** A distinctive two-zone fuel velocity configuration (inner and outer regions) designed to optimize heat removal from the central region of the core.
* **Control System:** Nine Hafnium absorber control rods enclosed in Hastelloy N guide tubes.

## Reference design

The GFMR is fuelled with FUNaK and moderated with graphite, with the fuel flowing through graphite channels from the bottom of the reactor to the top. The reactor has a height of 360 cm and a reflector diameter of 350 cm, with 379 fuel channels of 4 cm in diameter arranged in a hexagonal lattice, and delivers a thermal power of 150 MW.

A distinctive feature of the design is the presence of two distinct zones, an inner and an outer region, which differ only in the fuel velocity: a higher velocity is prescribed in the inner zone to enhance heat removal from the hotter central region of the core.

Nine control rods, each consisting of a 0.2 cm thick Hastelloy N guide tube that separates the fuel salt from a hafnium absorber of 1.3 cm in diameter, are placed directly inside the fuel channels; a 0.1 cm helium gap is left between the guide tube and the absorber to enable its withdrawal and insertion, and during nominal operation the control rods are assumed to be inserted to a depth of 36 cm.

## Provenance

Initially developed during the master thesis work by Thomas Sclauzero at Saltfoss Energy ApS under the supervision and guidance of Lubomír Bureš.

© 2026 Saltfoss Energy ApS. See [references and citation](references.md) for attribution.

## Benchmark results

Reference results will be added in a future update. This publication currently specifies the reference problem; it does not yet provide results for comparison.

[Continue to design parameters →](parameters.md){ .md-button }
