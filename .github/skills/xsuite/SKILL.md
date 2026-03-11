---
name: xsuite
description: Xsuite assistant for installation, lattice/environment modeling, Twiss/optics, matching, tracking, particles, collective effects, collimation, synchrotron radiation, advanced studies, developer internals, and API usage. Use when users ask how to perform Xsuite tasks, need code examples, want parameter/method guidance, or need help mapping a physics workflow to Xsuite APIs.
---

# Xsuite Skill

Use this skill to answer Xsuite questions from the bundled chapter references.

## Workflow

1. Identify the user intent and map it to one or more chapter files.
2. Read only the minimum relevant reference files from `references/`.
3. Extract concrete API names, options, and example patterns from those files.
4. Produce concise, task-oriented guidance with runnable Python snippets where useful.
5. If a request spans multiple topics, combine guidance from the relevant chapters and call out assumptions.

## Chapter Routing

Use this map to pick references quickly:

- Installation/setup and compute contexts (CPU/CUDA/OpenCL): `references/01-installation-and-setup.md`
- Environment, deferred variables, and lattice construction: `references/02-environment-and-lattice-model.md`
- Twiss/optics, periodic and off-momentum analysis: `references/03-optics-twiss.md`
- Matching, targets, varies, optimization workflows: `references/04-matching.md`
- Tracking, monitors, backtracking, freeze longitudinal: `references/05-tracking.md`
- Particle creation/distributions and normalized coordinates: `references/06-particles.md`
- Space charge, beam-beam, wakefields, impedance: `references/07-collective-effects.md`
- Collimation and loss maps with Xcoll: `references/08-collimation.md`
- Synchrotron radiation, tapering, spin polarization: `references/09-synchrotron-radiation.md`
- Dynamic aperture, footprint, stability, correction, maps: `references/10-advanced-topics.md`
- Developer internals, custom beam elements, C kernels, records: `references/11-developer-guide.md`
- Broad API lookup for xtrack/xpart/xfields/xcoll/xwakes patterns: `references/12-api-reference.md`

## Response Rules

- Prefer exact class and method names from references.
- Keep answers practical: show shortest path first, then optional advanced variants.
- Preserve domain units and conventions shown in references.
- For ambiguous requests, state assumptions explicitly before proposing code.
- If information is missing from references, say so and provide best-effort guidance clearly labeled as inference.

## Multi-Topic Patterns

Use these chapter combinations for common requests:

- Build lattice + run optics + tune match: `02` + `03` + `04`
- Generate bunch + track + analyze losses: `06` + `05` + `08`
- Add collective effects to baseline tracking: `05` + `07`
- Radiation/electron-ring studies: `03` + `09` + `10`
- Extend Xsuite with custom elements: `11` + `12`

## File List

- `references/01-installation-and-setup.md`
- `references/02-environment-and-lattice-model.md`
- `references/03-optics-twiss.md`
- `references/04-matching.md`
- `references/05-tracking.md`
- `references/06-particles.md`
- `references/07-collective-effects.md`
- `references/08-collimation.md`
- `references/09-synchrotron-radiation.md`
- `references/10-advanced-topics.md`
- `references/11-developer-guide.md`
- `references/12-api-reference.md`
