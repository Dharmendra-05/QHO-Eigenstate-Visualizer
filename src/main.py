# main.py
"""
QHO Visualizer
==============
Generates a publication-quality, dual-panel figure of the Quantum
Harmonic Oscillator eigenstates. Intended for WSL/headless environments;
uses plt.savefig exclusively (no plt.show).

Output naming is sequential — each run produces a new uniquely numbered
file inside the 'assets/' directory:
    assets/qho_plot_00.png
    assets/qho_plot_01.png
    assets/qho_plot_02.png
    ...

Run:
    python main.py
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D

from engine import QuantumHarmonicOscillator


# ── Configuration ─────────────────────────────────────────────────────────────
# All physical and visual parameters are declared here for easy adjustment.

N_STATES: int = 4                          # Number of energy levels to render
X_MIN: float = -6.0                        # Left bound of position axis
X_MAX: float = 6.0                         # Right bound of position axis
N_POINTS: int = 2000                       # Spatial resolution
ASSETS_DIR: str = "Assets"                 # Output directory for all saved figures
OUTPUT_STEM: str = "qho_plot"              # Base name; a numeric suffix is appended

# Physical parameters (natural units: ℏ=1, m=1, ω=1)
MASS: float = 1.0
OMEGA: float = 1.0
HBAR: float = 1.0

# Visual scaling factor for wavefunctions/densities plotted on the energy axis.
# Increase to make curves taller; decrease if they overlap.
AMPLITUDE_SCALE: float = 0.45

# Colormap: one perceptually distinct color per energy level.
# 'plasma' works well in both color and greyscale (for print).
CMAP_NAME: str = "plasma"


# ── Matplotlib Style ───────────────────────────────────────────────────────────
plt.rcParams.update(
    {
        "text.usetex": False,          # Set True if a full LaTeX distro is installed
        "mathtext.fontset": "cm",      # Computer Modern math font (LaTeX aesthetic)
        "font.family": "serif",
        "font.size": 12,
        "axes.labelsize": 14,
        "axes.titlesize": 15,
        "legend.fontsize": 11,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "figure.dpi": 150,
    }
)


# ── Sequential File Naming ─────────────────────────────────────────────────────

def get_next_output_path(assets_dir: str, stem: str, ext: str = "png") -> str:
    """
    Scans `assets_dir` for existing files matching `stem_NN.ext` and returns
    the next available path with a zero-padded two-digit suffix.

    Examples:
        No files exist      → assets/qho_plot_00.png
        _00 exists          → assets/qho_plot_01.png
        _00, _01 exist      → assets/qho_plot_02.png

    Args:
        assets_dir (str): Directory to scan and write into.
        stem (str): Base filename without suffix or extension.
        ext (str): File extension without the leading dot. Default: "png".

    Returns:
        str: The full path for the next output file.
    """
    os.makedirs(assets_dir, exist_ok=True)

    pattern = os.path.join(assets_dir, f"{stem}_*.{ext}")
    existing = sorted(glob.glob(pattern))

    if not existing:
        next_index = 0
    else:
        # Extract the numeric suffix from the last found file
        last_file = os.path.basename(existing[-1])
        # Strip stem + underscore prefix and extension suffix
        suffix_part = last_file[len(stem) + 1 : -(len(ext) + 1)]
        try:
            next_index = int(suffix_part) + 1
        except ValueError:
            # Fallback: use total count if suffix isn't cleanly numeric
            next_index = len(existing)

    filename = f"{stem}_{next_index:02d}.{ext}"
    return os.path.join(assets_dir, filename)


# ── Plot Helpers ───────────────────────────────────────────────────────────────

def get_colors(n: int, cmap_name: str) -> list:
    """Samples `n` perceptually uniform colors from a Matplotlib colormap."""
    cmap = plt.get_cmap(cmap_name)
    # Sample from 0.15→0.85 to avoid the very dark/light ends of the map
    return [cmap(v) for v in np.linspace(0.15, 0.85, n)]


def draw_harmonic_potential(
    ax: plt.Axes, x: np.ndarray, qho: QuantumHarmonicOscillator
) -> None:
    """
    Overlays the parabolic potential V(x) = (1/2)mω²x² on an axes object.

    Clipping the potential to the visible energy range prevents the parabola
    from dominating the figure at large |x|.
    """
    V = 0.5 * qho.mass * qho.omega**2 * x**2
    ax.plot(
        x, V,
        color="0.35", lw=1.5, ls="--", zorder=1,
        label=r"$V(x) = \frac{1}{2}m\omega^2 x^2$",
    )


def plot_wavefunctions(
    ax: plt.Axes,
    x: np.ndarray,
    qho: QuantumHarmonicOscillator,
    n_states: int,
    colors: list,
    scale: float,
) -> None:
    """
    Plots ψ_n(x) offset vertically by its energy eigenvalue E_n.

    Each wavefunction is drawn as a filled curve centered on its energy
    level — a standard textbook convention for direct visual comparison
    of spatial extent vs. quantized energy.
    """
    for n in range(n_states):
        E_n = qho.energy_level(n)
        psi = qho.wavefunction(n, x)
        y = E_n + scale * psi

        ax.plot(x, y, color=colors[n], lw=2.0, zorder=3)
        ax.fill_between(
            x, E_n, y, where=(y >= E_n),
            color=colors[n], alpha=0.35, zorder=2,
        )
        ax.fill_between(
            x, E_n, y, where=(y < E_n),
            color=colors[n], alpha=0.15, zorder=2,
        )

        # Dotted line at the energy level between turning points
        x_tp = qho.classical_turning_point(n)
        ax.hlines(E_n, -x_tp, x_tp, color=colors[n], lw=1.0, ls=":", alpha=0.8, zorder=2)

        # Right-margin energy annotation
        ax.text(
            X_MAX * 0.97, E_n,
            rf"$E_{n} = {E_n:.2f}\,\hbar\omega$",
            va="center", ha="right", fontsize=9.5, color=colors[n],
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.7),
        )


def plot_probability_densities(
    ax: plt.Axes,
    x: np.ndarray,
    qho: QuantumHarmonicOscillator,
    n_states: int,
    colors: list,
    scale: float,
) -> None:
    """
    Plots |ψ_n(x)|² offset vertically by E_n.

    Vertical dashed lines at the classical turning points make quantum
    tunneling directly visible — the probability density is non-zero
    in the classically forbidden region beyond these lines.
    """
    for n in range(n_states):
        E_n = qho.energy_level(n)
        prob = qho.probability_density(n, x)
        y = E_n + scale * prob

        ax.plot(x, y, color=colors[n], lw=2.0, zorder=3)
        ax.fill_between(x, E_n, y, color=colors[n], alpha=0.4, zorder=2)

        # Classical turning points
        x_tp = qho.classical_turning_point(n)
        ax.hlines(E_n, -x_tp, x_tp, color=colors[n], lw=1.0, ls=":", alpha=0.8, zorder=2)
        for sign in [-1, 1]:
            ax.axvline(
                sign * x_tp, color=colors[n], lw=0.75, ls="--", alpha=0.5, zorder=1
            )


def build_legend(colors: list, n_states: int) -> list:
    """Creates custom legend handles, one per energy level."""
    return [
        Line2D([0], [0], color=colors[n], lw=2.5, label=rf"$n = {n}$")
        for n in range(n_states)
    ]


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    """Main entry point: builds the dual-panel QHO figure and saves it."""

    # ── Physics Setup ──────────────────────────────────────────────────────────
    qho = QuantumHarmonicOscillator(mass=MASS, omega=OMEGA, hbar=HBAR)
    x = np.linspace(X_MIN, X_MAX, N_POINTS)
    colors = get_colors(N_STATES, CMAP_NAME)

    # ── Figure Layout ──────────────────────────────────────────────────────────
    fig, axes = plt.subplots(
        1, 2,
        figsize=(14, 7),
        sharey=True,
        gridspec_kw={"wspace": 0.05},
    )
    ax_psi, ax_prob = axes

    # ── Left Panel: Wavefunctions ──────────────────────────────────────────────
    draw_harmonic_potential(ax_psi, x, qho)
    plot_wavefunctions(ax_psi, x, qho, N_STATES, colors, AMPLITUDE_SCALE)

    ax_psi.set_title(r"Wavefunctions $\psi_n(x)$")
    ax_psi.set_xlabel(r"Position $x$ (natural units)")
    ax_psi.set_ylabel(r"Energy $E\,/\,\hbar\omega$")
    ax_psi.set_xlim(X_MIN, X_MAX)
    ax_psi.set_ylim(-0.3, N_STATES + 0.5)
    ax_psi.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax_psi.grid(alpha=0.2, zorder=0)
    legend_handles = build_legend(colors, N_STATES)
    ax_psi.legend(handles=legend_handles, loc="upper left", framealpha=0.85)

    # ── Right Panel: Probability Densities ────────────────────────────────────
    draw_harmonic_potential(ax_prob, x, qho)
    plot_probability_densities(ax_prob, x, qho, N_STATES, colors, AMPLITUDE_SCALE)

    ax_prob.set_title(r"Probability Densities $|\psi_n(x)|^2$")
    ax_prob.set_xlabel(r"Position $x$ (natural units)")
    ax_prob.set_xlim(X_MIN, X_MAX)
    ax_prob.grid(alpha=0.2, zorder=0)

    potential_handle = Line2D(
        [0], [0], color="0.35", lw=1.5, ls="--",
        label=r"$V(x)=\frac{1}{2}m\omega^2x^2$",
    )
    ax_prob.legend(handles=[potential_handle], loc="upper left", framealpha=0.85)

    # ── Global Title ───────────────────────────────────────────────────────────
    fig.suptitle(
        r"Quantum Harmonic Oscillator — Eigenstates ($m=1,\;\omega=1,\;\hbar=1$)",
        fontsize=16,
        y=1.01,
    )

    # ── Sequential Save ────────────────────────────────────────────────────────
    output_path = get_next_output_path(ASSETS_DIR, OUTPUT_STEM)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"[✓] Figure saved → '{output_path}' (300 dpi)")

    plt.close(fig)  # Free memory — important when running in a loop


if __name__ == "__main__":
    main()
