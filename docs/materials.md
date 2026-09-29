---
title: Materials
eyebrow: MATERIALS / PROPERTIES & DEFINITIONS
source: "Source: GFMR reference, Materials, Listings 1–5 (pp. 2–4)."
---

# Materials

Material properties and OpenMC definitions from the GFMR reference.
{ .lead }

## FUNaK fuel { #funak }

Fuel salt. Reference [1](references.md#ref-1).

### Material properties

| Property | Specification |
| :--- | :--- |
| Composition | 26.4 UF<sub>4</sub> – 24.7 KF – 48.9 NaF mol% |
| Density | ρ = 4.808 − 0.00113 T g/cm<sup>3</sup>, T in °C |
| Viscosity | η = 736.58 exp(−0.006 T) mPa s, T in °C |
| Heat capacity | C<sub>p</sub> = 900 J kg<sup>−1</sup> K<sup>−1</sup> |

### OpenMC definition

```python title="Listing 1 · FUNaK fuel"
fuel = openmc.Material(name='fuel')
fuel.add_element('Na', 0.1751432664756447, 'ao')
fuel.add_element('K', 0.08846704871060172, 'ao')
fuel.add_element('F', 0.6418338108882521, 'ao')
fuel.add_element('U', 0.094555874, 'ao', enrichment=enrichment)
density_fuel = 4.808 - 0.00113 * (temperature_fuel_C)
fuel.set_density('g/cm3', density_fuel)
fuel.temperature = temperature_fuel_K
```

## Graphite { #graphite }

Moderator / reflector. References [2](references.md#ref-2), [3](references.md#ref-3).

### Material properties

| Property | Specification |
| :--- | :--- |
| Thermal conductivity | K = 25 W m<sup>−1</sup> K<sup>−1</sup> |

### OpenMC definition

```python title="Listing 2 · Graphite moderator"
moderator = openmc.Material(name='graphite')
moderator.add_element('C', 0.999999)
moderator.add_element('B', 0.000001)
moderator.set_density('g/cm3', 1.7)
moderator.add_s_alpha_beta('c_Graphite')
moderator.temperature = t_graphite_K
```

## Hafnium { #hafnium }

Absorber. Reference [4](references.md#ref-4).

The absorber is modeled as pure hafnium.

### OpenMC definition

```python title="Listing 3 · Hafnium absorber"
absorber = openmc.Material(name='control_rod')
absorber.add_element('Hf', 1.0, 'ao')
absorber.set_density('g/cm3', 13.3)
absorber.temperature = temperature_fuel_K
```

## Hastelloy N { #hastelloy-n }

Guide tube. Reference [5](references.md#ref-5).

The guide tube material is specified through elemental weight fractions corresponding to a nominal Hastelloy N composition.

### OpenMC definition

```python title="Listing 4 · Hastelloy N guide tube"
guide_tube_material.add_element('Ni', 71, percent_type='wo')
guide_tube_material.add_element('Cr', 7, percent_type='wo')
guide_tube_material.add_element('Mo', 16, percent_type='wo')
guide_tube_material.add_element('Fe', 4, percent_type='wo')
guide_tube_material.add_element('Si', 1, percent_type='wo')
guide_tube_material.add_element('Mn', 0.8, percent_type='wo')
guide_tube_material.add_element('V', 0.2, percent_type='wo')
guide_tube_material.set_density('g/cm3', 8.86)
guide_tube_material.temperature = temperature_fuel_K
```

## Helium { #helium }

Gap. Reference [6](references.md#ref-6).

The channel gap is modeled using helium.

### OpenMC definition

```python title="Listing 5 · Helium gap"
helium = openmc.Material(name='helium')
helium.add_element('He', 1.0)
helium.set_density('g/cm3', 0.0001785)
helium.temperature = temperature_fuel_K
```

The listings above are excerpts from the reference, with typographic quotation marks converted to code quotation marks. They retain the variable names and values in the source; they are not standalone programs.
{ .source-note }
