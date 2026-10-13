---
title: Design parameters
eyebrow: MODEL / DESIGN PARAMETERS
---

<!--
docs/parameters.md — Design parameters of the GFMR reference model.

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

# Design parameters

The main geometrical and design parameters of the GFMR reference model.
{ .lead }

## Main design parameters

| Parameter | Value |
| :--- | ---: |
| Power | 150 MW |
| Height | 3.6 m |
| Fuel temperature | 650 °C |
| Mass flow rate | 2300 kg s<sup>−1</sup> |
| Enrichment | 2.12 % |
| Core diameter | 3.5 m |
| Fuel channel diameter | 4.0 cm |
| Graphite temperature | 800 °C |
| Hexagon pitch | 14 cm |
| Control rod insertion | 36 cm nominal |

The 3.5 m dimension is the **reflector diameter** in the geometry description and is labelled **core diameter** in the main design parameters.

## Core configuration

The core contains **379 fuel channels** arranged in a hexagonal lattice. Fuel flows through the graphite channels from the bottom of the reactor to the top.

The inner and outer regions differ only in fuel velocity. The higher inner-zone velocity enhances heat removal from the hotter central region of the core. See [channel hydraulics](hydraulics.md) for the specified values.

## Control rod channel geometry

Nine control rods are placed directly inside the fuel channels. Each Hastelloy N guide tube separates the fuel salt from a hafnium absorber. A helium gap between the guide tube and absorber enables withdrawal and insertion.

| Parameter | Value |
| :--- | ---: |
| Control rod channel diameter | 4.0 cm |
| Absorber diameter | 1.3 cm |
| Guide tube thickness | 0.2 cm |
| Void gap thickness | 0.1 cm |

During nominal operation, the control rods are assumed to be inserted to a depth of **36 cm**.

[View the control rod geometry →](geometry.md#control-rod-channel){ .md-button }
