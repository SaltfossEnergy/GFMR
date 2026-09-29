---
title: Model overview
eyebrow: THE MODEL / OVERVIEW
source: "Sources: supplied GFMR Model text; GFMR reference, Introduction (p. 1)."
---

# Model overview

Generic FUNaK-Fuelled Thermal Molten Salt Reactor (GFMR) Model
{ .lead }

## Overview

This repository provides the design and geometrical specifications for a Generic FUNaK-Fuelled Thermal Molten Salt Reactor (GFMR). The GFMR is intended as a reference problem for the modeling and simulation of molten salt reactors, capturing many of the essential physical phenomena relevant to graphite-moderated MSR systems.

<div class="reference-notice" markdown>

--8<-- "notice.md"

</div>

The model is described in detail in the attached PDF document. It is designed to be software-agnostic and can be implemented using a single-physics approach or within a complex multiphysics framework.

## Key Model Features

* **Fuel & Moderator:** Utilizes FUNaK fuel salt with graphite moderation.
* **Thermal Power:** 150 MW.
* **Core Geometry:** A reactor height of 360 cm and a reflector diameter of 350 cm, featuring 379 fuel channels arranged in a hexagonal lattice.
* **Zoned Velocity:** A distinctive two-zone fuel velocity configuration (inner and outer regions) designed to optimize heat removal from the central region of the core.
* **Control System:** Nine Hafnium absorber control rods enclosed in Hastelloy N guide tubes.

## Introduction from the reference

This paper reports the main geometrical and design parameters of the GFMR, a reference problem proposed for the modelling of molten salt reactors. The GFMR is fuelled with FUNaK and moderated with graphite, with the fuel flowing through graphite channels from the bottom of the reactor to the top. The reactor has a height of 360 cm and a reflector diameter of 350 cm, with 379 fuel channels of 4 cm in diameter arranged in a hexagonal lattice, and delivers a thermal power of 150 MW.

A distinctive feature of the design is the presence of two distinct zones, an inner and an outer region, which differ only in the fuel velocity: a higher velocity is prescribed in the inner zone to enhance heat removal from the hotter central region of the core.

Nine control rods, each consisting of a 0.2 cm thick Hastelloy N guide tube that separates the fuel salt from a hafnium absorber of 1.3 cm in diameter, are placed directly inside the fuel channels; a 0.1 cm helium gap is left between the guide tube and the absorber to enable its withdrawal and insertion, and during nominal operation the control rods are assumed to be inserted to a depth of 36 cm.

## Disclaimer

--8<-- "disclaimer.md"

[Continue to design parameters →](parameters.md){ .md-button }
