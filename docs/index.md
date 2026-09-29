---
title: GFMR — A reference model for molten salt reactors
template: home.html
hide:
  - toc
---

<section class="hero" markdown>
<div class="hero__copy" markdown>

<p class="eyebrow"><span class="status-dot" aria-hidden="true"></span>GFMR / REFERENCE MODEL</p>

# A reference model for molten salt reactors.

Generic FUNaK-Fuelled Thermal Molten Salt Reactor
{ .hero__subtitle }

A reference problem for the modelling and simulation of graphite-moderated molten salt reactors. A benchmark and educational tool for the broader nuclear engineering community.
{ .hero__intro }

<div class="hero__actions" markdown>

[Explore the model <span aria-hidden="true">↗</span>](overview.md){ .md-button .md-button--primary }
[View the geometry <span aria-hidden="true">→</span>](geometry.md){ .text-link }

</div>

<p class="hero__authors">Thomas Sclauzero <span aria-hidden="true">/</span> Lubomír Bureš</p>

</div>
<div class="hero__visual" markdown>

<div class="figure-label"><span>01 / CORE GEOMETRY</span><span>TOP VIEW · x–y</span></div>

[![Top view of the GFMR reactor core, with fuel channels in orange and graphite in grey.](assets/images/geometry-xy.png){ width="3870" height="3896" fetchpriority="high" }](geometry.md#top-view)

<div class="figure-label figure-label--bottom"><span>379 FUEL CHANNELS</span><span>HEXAGONAL LATTICE</span></div>

</div>
</section>

<section class="reference-notice" aria-label="Important model notice" markdown>

--8<-- "notice.md"

[Read the disclaimer →](disclaimer.md)

</section>

<div class="stat-strip" aria-label="Key design parameters" markdown>
<div class="stat" markdown>

<span class="stat__value">150 <span>MW</span></span>
<span class="stat__label">THERMAL POWER</span>

</div>
<div class="stat" markdown>

<span class="stat__value">379</span>
<span class="stat__label">FUEL CHANNELS</span>

</div>
<div class="stat" markdown>

<span class="stat__value">3.6 <span>m</span></span>
<span class="stat__label">REACTOR HEIGHT</span>

</div>
<div class="stat" markdown>

<span class="stat__value">2</span>
<span class="stat__label">FUEL VELOCITY ZONES</span>

</div>
</div>

<section class="home-section" markdown>
<div class="section-heading" markdown>

<p class="eyebrow">THE DOCUMENTATION</p>

## Explore the reference design.

Geometrical specifications, design parameters, and material definitions for the GFMR model.

</div>

<div class="document-grid" markdown>
<div class="document-card" markdown>

<span class="card-number">01 / MODEL</span>

### Design & parameters

Thermal power, temperatures, channel velocities, pressure losses, and the core lifetime criterion.

[Read the specifications <span aria-hidden="true">↗</span>](parameters.md)

</div>
<div class="document-card" markdown>

<span class="card-number">02 / GEOMETRY</span>

### Inside the core

Top and lateral views of the reactor, with a closer look at the control rod channel.

[Explore the geometry <span aria-hidden="true">↗</span>](geometry.md)

</div>
<div class="document-card" markdown>

<span class="card-number">03 / MATERIALS</span>

### Material definitions

FUNaK fuel salt, graphite, hafnium, Hastelloy N, and helium, including the source OpenMC definitions.

[Browse the materials <span aria-hidden="true">↗</span>](materials.md)

</div>
</div>
</section>

<section class="study-panel" markdown>
<div markdown>

<p class="eyebrow">MODELLING & SIMULATION</p>

## One reference.<br>Different approaches.

</div>
<div markdown>

The model is designed to be software-agnostic and can be implemented using a single-physics approach or within a complex multiphysics framework.

[Read the model overview <span aria-hidden="true">→</span>](overview.md){ .text-link }

</div>
</section>
