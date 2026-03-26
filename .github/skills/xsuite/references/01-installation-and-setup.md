# Xsuite: Installation and Setup

## Overview

Xsuite is a collection of Python packages for the simulation of beam dynamics in particle accelerators. It supports different computing platforms including CPUs and GPUs (via CUDA and OpenCL). The suite is modular, with each package handling a specific aspect of beam dynamics simulation.

### Packages

- **Xobjects**: Memory management, code compilation and execution on different computing platforms (CPU, GPU).
- **Xpart**: Particle ensemble generation and manipulation.
- **Xtrack**: Single-particle tracking, beam line creation, and import from external formats.
- **Xfields**: Electromagnetic field computation including PIC (Particle-In-Cell) solvers and analytical distributions.
- **Xdeps**: Dependency management and deferred expressions for parameter relationships.
- **Xcoll**: Particle-matter interaction simulation with native routines and interfaces to FLUKA and Geant4.
- **Xwakes**: Wakefield and impedance elements for collective effects modeling.

---

## Installation

### Basic Installation (CPU only)

For CPU-only usage, install xsuite directly from PyPI:

```bash
pip install xsuite
```

This installs all core xsuite packages (xobjects, xtrack, xpart, xfields, xdeps, xcoll, xwakes) and their dependencies.

### GPU Support (CUDA / NVIDIA)

To use NVIDIA GPUs, install CuPy for your CUDA version before installing xsuite:

```bash
# For CUDA 11.x
pip install cupy-cuda11x
pip install xsuite

# For CUDA 12.x
pip install cupy-cuda12x
pip install xsuite
```

### GPU Support (OpenCL)

To use GPUs (or other accelerators) via OpenCL, install PyOpenCL before installing xsuite:

```bash
pip install pyopencl
pip install xsuite
```

### Development Installation

For development or to work with the latest source code, clone each package repository and install in editable mode:

```bash
git clone https://github.com/xsuite/xobjects
git clone https://github.com/xsuite/xpart
git clone https://github.com/xsuite/xtrack
git clone https://github.com/xsuite/xfields
git clone https://github.com/xsuite/xdeps
git clone https://github.com/xsuite/xcoll

pip install -e xobjects
pip install -e xpart
pip install -e xtrack
pip install -e xfields
pip install -e xdeps
pip install -e xcoll
```

---

## Contexts (Computing Platforms)

Xsuite uses "contexts" to abstract the computing platform. A context manages memory allocation, data transfer, and kernel execution on a given device. Three context types are available:

### Available Contexts

| Context | Description |
|---|---|
| `xo.ContextCpu()` | CPU execution, single-threaded (default) |
| `xo.ContextCpu(omp_num_threads=N)` | CPU execution with OpenMP multithreading using N threads |
| `xo.ContextCpu(omp_num_threads='auto')` | CPU execution with OpenMP using maximum available threads |
| `xo.ContextCupy()` | NVIDIA GPU execution via CUDA/CuPy |
| `xo.ContextPyopencl()` | GPU or CPU execution via PyOpenCL |

### Example Usage

```python
import xobjects as xo
import xtrack as xt

# Choose one of the following contexts:
context = xo.ContextCpu()                        # CPU, single-threaded
# context = xo.ContextCpu(omp_num_threads=4)     # CPU, 4 OpenMP threads
# context = xo.ContextCpu(omp_num_threads='auto') # CPU, max OpenMP threads
# context = xo.ContextCupy()                     # NVIDIA GPU (CUDA)
# context = xo.ContextPyopencl()                 # GPU/CPU (OpenCL)

# Build tracker on the chosen context
line.build_tracker(_context=context)
```

Contexts are interchangeable: the same simulation code works across all supported platforms without modification. Switching from CPU to GPU execution requires only changing the context.

---

## Getting Started - Quick Example

The following example demonstrates creating a simple lattice, generating particles, tracking, and accessing results:

```python
import numpy as np
import xtrack as xt

# Create a simple FODO-like lattice
line = xt.Line(
    elements=[xt.Drift(length=2.),
              xt.Multipole(knl=[0, 0.5], ksl=[0, 0]),
              xt.Drift(length=1.),
              xt.Multipole(knl=[0, -0.5], ksl=[0, 0])],
    element_names=['drift_0', 'quad_0', 'drift_1', 'quad_1'])

# Set the reference particle (proton at 6.5 TeV/c)
line.set_particle_ref('proton', p0c=6.5e12)

# Build a particle ensemble
n_part = 200
particles = line.build_particles(
    x=np.random.uniform(-1e-3, 1e-3, n_part),
    px=np.random.uniform(-1e-5, 1e-5, n_part),
    y=np.random.uniform(-2e-3, 2e-3, n_part),
    py=np.random.uniform(-3e-5, 3e-5, n_part),
    zeta=np.random.uniform(-1e-2, 1e-2, n_part),
    delta=np.random.uniform(-1e-4, 1e-4, n_part))

# Track particles for 100 turns
line.track(particles, num_turns=100)

# Access results
print(particles.x)     # x coordinates after tracking
print(particles.state)  # > 0 for alive particles
```

---

## Key Imports

Each xsuite package has a conventional import alias:

```python
import xobjects as xo   # Memory and context management
import xtrack as xt      # Tracking engine, lattice construction
import xpart as xp       # Particle generation (also re-exported via xtrack)
import xfields as xf     # Collective effects, electromagnetic fields
import xcoll as xc       # Collimation studies
import xwakes as xw      # Wakefields and impedance
```

In most workflows, `xtrack` is the primary package. It re-exports particle generation functionality from `xpart`, so importing `xpart` separately is often unnecessary unless advanced particle manipulation is needed.

---

## Combined CPU-GPU Simulations

When running simulations on GPU, certain elements (for example, PyHEADTAIL-based elements) may not support GPU execution. These elements can be flagged to run on CPU by setting the `needs_cpu` attribute on them. Xtrack handles the necessary data transfers between GPU and CPU memory automatically and transparently, so no manual data movement is required.

---

## Data Management

Xsuite can download and cache test data and lattice files for use in simulations and examples.

- **Default cache location**: `~/.local/share/xsuite/`
- **Override via environment variable**: Set `XSUITE_DATA_DIR` to specify a custom cache directory.

```bash
# Example: set a custom data directory
export XSUITE_DATA_DIR=/path/to/custom/xsuite/data
```

This is useful in shared computing environments or when disk space on the home directory is limited.
