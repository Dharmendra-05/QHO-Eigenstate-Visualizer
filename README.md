# ⚛️ Computational Physics Toolbox
### A Professional-Grade Quantum Mechanics Simulation & Visualization Suite

<p align="center">
  <img src="assets/qho_plot_00.png" alt="QHO Eigenstates Plot" width="900"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/NumPy-2.4-013243?style=for-the-badge&logo=numpy&logoColor=white"/>
  <img src="https://img.shields.io/badge/SciPy-1.17-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white"/>
  <img src="https://img.shields.io/badge/Matplotlib-3.10-11557C?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [The Physics](#-the-physics)
- [Project Architecture](#-project-architecture)
- [Features](#-features)
- [Output](#-output)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Visualizer](#running-the-visualizer)
- [API Reference](#-api-reference)
- [Configuration & Customization](#-configuration--customization)
- [Roadmap](#-roadmap)
- [References](#-references)
- [License](#-license)

---

## 🔭 Overview

The **Computational Physics Toolbox** is a modular, object-oriented Python suite for simulating and visualizing quantum mechanical systems to a publication-ready standard. The first module in this toolbox is a full solver and visualizer for the **1D Quantum Harmonic Oscillator (QHO)** — one of the most fundamental and exactly solvable problems in all of quantum mechanics.

This project was built with professional software engineering principles at its core: a clean separation between the physics engine and the visualization layer, strict type hinting, Google-style docstrings, and parameterized physical constants throughout.

> **Intended Audience:** Physics students, researchers, and educators who need high-fidelity, scriptable, and extensible quantum mechanics visualizations.

---

## ⚛️ The Physics

The **1D Quantum Harmonic Oscillator** describes a particle of mass $m$ in a parabolic potential well:

$$V(x) = \frac{1}{2}m\omega^2 x^2$$

Its Hamiltonian is:

$$\hat{H} = \frac{\hat{p}^2}{2m} + \frac{1}{2}m\omega^2\hat{x}^2$$

The time-independent Schrödinger equation $\hat{H}\psi = E\psi$ yields an infinite ladder of **exact, analytic eigenstates**:

$$\psi_n(x) = \mathcal{N}_n \cdot H_n\!\left(\frac{x}{x_0}\right) \cdot \exp\!\left(-\frac{x^2}{2x_0^2}\right)$$

where:

| Symbol | Meaning |
|---|---|
| $\mathcal{N}_n = \frac{1}{\sqrt{2^n \, n! \, x_0 \sqrt{\pi}}}$ | Normalization constant ensuring $\int_{-\infty}^{\infty} \|\psi_n\|^2 \, dx = 1$ |
| $H_n(\xi)$ | Physicists' Hermite polynomial of degree $n$ |
| $x_0 = \sqrt{\hbar / m\omega}$ | Characteristic length scale of the oscillator |

The **quantized energy eigenvalues** are:

$$\boxed{E_n = \left(n + \frac{1}{2}\right)\hbar\omega, \quad n = 0, 1, 2, \ldots}$$

The $\frac{1}{2}\hbar\omega$ **zero-point energy** at $n=0$ is a profound consequence of the **Heisenberg Uncertainty Principle** — the particle can never be at rest, even at absolute zero temperature. Classically, the particle would be stationary at the potential minimum. Quantum mechanically, it fluctuates forever.

The **classical turning points** $x_{tp} = \sqrt{2E_n / m\omega^2}$, where $E_n = V(x_{tp})$, are marked on the probability density plot. The non-zero value of $|\psi_n|^2$ beyond these points is a direct visualization of **quantum tunneling**.

---

## 🏗️ Project Architecture

The project strictly separates **physics computation** from **visualization**, ensuring each module is independently testable and reusable.

```
computational-physics-toolbox/
│
├── engine.py               # ⚙️  Pure physics backend — zero plotting imports
│   └── QuantumHarmonicOscillator (class)
│       ├── wavefunction(n, x)
│       ├── probability_density(n, x)
│       ├── energy_level(n)
│       └── classical_turning_point(n)
│
├── main.py                 # 🎨  Visualization & execution layer
│   ├── get_next_output_path()   ← sequential auto-naming
│   ├── plot_wavefunctions()
│   ├── plot_probability_densities()
│   ├── draw_harmonic_potential()
│   └── main()
│
├── assets/                 # 📁  All saved figures live here
│   ├── qho_plot_00.png     #     First run
│   ├── qho_plot_01.png     #     Second run (different config)
│   └── qho_plot_02.png     #     Third run, and so on...
│
├── requirements.txt        # 📦  Pinned dependencies
└── README.md               # 📖  This file
```

> **Design Principle:** `engine.py` contains zero Matplotlib imports. It can be imported by a Flask web app, a Jupyter notebook, or any other frontend without modification. Adding a new quantum system (e.g., Finite Potential Well) requires only adding a new class to `engine.py`.

---

## ✨ Features

- **Object-Oriented Physics Engine** — `QuantumHarmonicOscillator` class with full parameter control over mass $m$, angular frequency $\omega$, and $\hbar$.
- **Dual-Panel Publication Figure** — Side-by-side visualization of wavefunctions $\psi_n(x)$ and probability densities $|\psi_n(x)|^2$, vertically offset by their quantized energy levels.
- **Sequential Auto-Saving** — Each run automatically produces a new uniquely numbered file (`qho_plot_00.png`, `qho_plot_01.png`, …) inside the `assets/` directory. No run ever overwrites a previous result.
- **Classical Turning Points** — Automatically computed and annotated on the probability density panel, making quantum tunneling immediately visible.
- **LaTeX Math Rendering** — All axis labels, titles, and annotations use Matplotlib's Computer Modern math font for a genuine journal-quality aesthetic.
- **Perceptual Colormap** — Uses the `plasma` colormap, which is perceptually uniform and remains distinguishable in greyscale (for print).
- **Headless / WSL Compatible** — Uses `plt.savefig` exclusively; no GUI window is required.
- **Fully Parameterized** — All physical constants and visual settings are declared in a single configuration block at the top of `main.py`.
- **Strict Type Hinting & Docstrings** — Every public method has full Python type annotations and a Google-style docstring.

---

## 📊 Output

All figures are saved automatically to the `assets/` directory with sequential, zero-padded filenames. Each run of `python main.py` appends a new file — no previous output is ever overwritten.

```
assets/
├── qho_plot_00.png    ← n=0..3, plasma colormap (default)
├── qho_plot_01.png    ← n=0..5, viridis colormap
└── qho_plot_02.png    ← n=0..3, ω=0.5 (wider well)
```

Each figure is a 300 dpi, two-panel layout:

| Left Panel | Right Panel |
|---|---|
| Wavefunctions $\psi_n(x)$ for $n = 0 \ldots N{-}1$ | Probability Densities $\|\psi_n(x)\|^2$ for $n = 0 \ldots N{-}1$ |
| Offset vertically by $E_n$ | Offset vertically by $E_n$ |
| Parabolic potential $V(x)$ overlaid | Classical turning points marked |
| Energy level annotations on the right margin | Vertical dashed lines at $\pm x_{tp}$ |

---

## 🚀 Getting Started

### Prerequisites

- Python **3.10** or higher
- `pip` and `venv` (standard library)
- A terminal — works natively on Linux/macOS and on **WSL** (Windows Subsystem for Linux)

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/Dharmendra-05/QHO-Eigenstate-Visualizer.git
cd Quantum-Harmonic-Oscillator-Visualisation
```

**2. Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```
> On Windows (PowerShell, non-WSL): `venv\Scripts\Activate.ps1`

**3. Install all dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Visualizer

```bash
python main.py
```

On success, you will see the path of the newly created file:
```
[✓] Figure saved → 'assets/qho_plot_00.png' (300 dpi)
```

Run it again (e.g., after changing `N_STATES` or `OMEGA`) and it auto-increments:
```
[✓] Figure saved → 'assets/qho_plot_01.png' (300 dpi)
```

Open the output in WSL:
```bash
explorer.exe assets/qho_plot_00.png
```

---

## 📖 API Reference

### `class QuantumHarmonicOscillator` — `engine.py`

The core physics solver. Initialize with physical parameters, then call its methods over any position array.

```python
from engine import QuantumHarmonicOscillator
import numpy as np

# Natural units: ℏ = m = ω = 1 (default)
qho = QuantumHarmonicOscillator(mass=1.0, omega=1.0, hbar=1.0)

x = np.linspace(-6, 6, 1000)
```

#### `qho.wavefunction(n, x)` → `np.ndarray`

Returns $\psi_n(x)$, the $n$-th energy eigenstate wavefunction.

```python
psi_2 = qho.wavefunction(n=2, x=x)
```

#### `qho.probability_density(n, x)` → `np.ndarray`

Returns $|\psi_n(x)|^2$. Guaranteed non-negative; integrates to 1.

```python
prob_2 = qho.probability_density(n=2, x=x)
```

#### `qho.energy_level(n)` → `float`

Returns the exact energy eigenvalue $E_n = (n + \frac{1}{2})\hbar\omega$.

```python
E_2 = qho.energy_level(n=2)  # → 2.5 (in natural units)
```

#### `qho.classical_turning_point(n)` → `float`

Returns the positive classical turning point $x_{tp}$ where $V(x_{tp}) = E_n$.

```python
x_tp = qho.classical_turning_point(n=2)  # → 2.236...
```

#### Using SI Units

To simulate a physical system (e.g., a diatomic molecule modeled as a harmonic oscillator), pass SI values directly:

```python
from scipy.constants import hbar, atomic_mass

qho_si = QuantumHarmonicOscillator(
    mass=1.0 * atomic_mass,   # 1 amu in kg
    omega=1.0e13,              # ~infrared vibrational frequency in rad/s
    hbar=hbar                  # 1.0545718e-34 J·s
)
```

---

## ⚙️ Configuration & Customization

All tunable parameters live at the top of `main.py` under a clearly marked configuration block. No other part of the code needs to be touched.

```python
# ── Configuration ─────────────────────────────────────────────────────────────
N_STATES: int = 4               # Number of energy levels to render
X_MIN: float = -6.0             # Left bound of position axis
X_MAX: float = 6.0              # Right bound of position axis
N_POINTS: int = 2000            # Spatial resolution (increase for smoother curves)
ASSETS_DIR: str = "assets"      # Output directory — created automatically if absent
OUTPUT_STEM: str = "qho_plot"   # Base filename; a _NN suffix is appended each run

MASS: float = 1.0               # Particle mass (natural units)
OMEGA: float = 1.0              # Angular frequency ω
HBAR: float = 1.0               # Reduced Planck constant ℏ

AMPLITUDE_SCALE: float = 0.45   # Vertical scale of wavefunction curves
CMAP_NAME: str = "plasma"       # Any valid Matplotlib colormap name
```

**Common customizations:**

| Goal | Change |
|---|---|
| Show 6 energy levels | `N_STATES = 6` |
| Wider potential well ($\omega$ smaller) | `OMEGA = 0.5` |
| Use `viridis` colormap | `CMAP_NAME = "viridis"` |
| Higher-resolution output | `N_POINTS = 5000` |
| Save as PDF for publication | Change `ext="pdf"` in `get_next_output_path(...)` call |
| Change output folder name | `ASSETS_DIR = "figures"` |

---

## 🗺️ Roadmap

This toolbox is designed to grow. Planned modules follow the same `engine.py` / `main.py` architecture:

- [ ] **Finite Potential Well** — Numerically solved bound states and transmission coefficients
- [ ] **Particle in a Box** (1D & 2D) — Infinite square well eigenstates
- [ ] **Hydrogen Atom** — Radial wavefunctions $R_{nl}(r)$ and spherical harmonic visualizations
- [ ] **Quantum Tunneling** — Time-dependent wavepacket propagation through a barrier (split-step Fourier method)
- [ ] **Coupled Oscillators** — Normal modes and phonon dispersion relations
- [ ] **Interactive Dashboard** — Optional `ipywidgets` / Plotly frontend for Jupyter notebooks

---

## 📚 References

1. Griffiths, D. J. & Schroeter, D. F. (2018). *Introduction to Quantum Mechanics* (3rd ed.). Cambridge University Press.
2. Cohen-Tannoudji, C., Diu, B., & Laloë, F. (1977). *Quantum Mechanics* (Vol. 1). Wiley-VCH.
3. Sakurai, J. J. & Napolitano, J. (2021). *Modern Quantum Mechanics* (3rd ed.). Cambridge University Press.
4. SciPy Documentation — [`scipy.special.hermite`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.hermite.html)
5. Matplotlib Documentation — [*Colormap reference*](https://matplotlib.org/stable/gallery/color/colormap_reference.html)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this code for academic and commercial purposes with attribution.

---

<p align="center">
  Built with 🧠 and ☕ by a Physics Honours student who refuses to write unreadable code.<br/>
  <em>"If you think you understand quantum mechanics, you don't understand quantum mechanics." — R. Feynman</em>
</p>