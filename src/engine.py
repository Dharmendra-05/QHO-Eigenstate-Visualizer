# engine.py
"""
QHO Physics Engine
==================
Provides the core quantum mechanics computational backend.
This module is deliberately kept free of any plotting or I/O logic
to ensure it can be imported by any frontend (Matplotlib, web app, etc.)

Physics Primer:
    The 1D Quantum Harmonic Oscillator Hamiltonian is:
        H = p²/(2m) + (1/2)mω²x²
    Its exact, analytic eigenstates (stationary states) are:
        ψ_n(x) = N_n * H_n(ξ) * exp(-ξ²/2)
    where ξ = sqrt(mω/ℏ)·x is the dimensionless position coordinate,
    H_n is the physicists' Hermite polynomial of degree n, and N_n is
    the normalization constant ensuring ∫|ψ_n|²dx = 1.
    The quantized energy eigenvalues are:
        E_n = (n + 1/2)ℏω,  n = 0, 1, 2, ...
    The famous zero-point energy E_0 = ℏω/2 arises directly from the
    Heisenberg Uncertainty Principle — the particle can never be at rest.
"""

import math
import numpy as np
from scipy.special import hermite
from scipy.constants import hbar as HBAR_SI
from typing import Optional


class QuantumHarmonicOscillator:
    """
    A solver for the 1D Quantum Harmonic Oscillator (QHO).

    This class encapsulates all physical parameters and provides clean
    methods for computing wavefunctions, probability densities, and energy
    eigenvalues. It supports both natural units (ℏ=1) for theoretical
    work and SI units for physical simulations.

    Attributes:
        mass (float): Particle mass in kg (SI) or natural units.
        omega (float): Angular frequency ω in rad/s (SI) or natural units.
        hbar (float): Reduced Planck constant. Defaults to ℏ=1 (natural units).

    Example:
        >>> qho = QuantumHarmonicOscillator(mass=1.0, omega=1.0)
        >>> x = np.linspace(-5, 5, 500)
        >>> psi_0 = qho.wavefunction(n=0, x=x)
        >>> E_0 = qho.energy_level(n=0)
    """

    def __init__(
        self,
        mass: float = 1.0,
        omega: float = 1.0,
        hbar: float = 1.0,
    ) -> None:
        """
        Initializes the QHO with its defining physical parameters.

        Args:
            mass (float): Particle mass. Default is 1.0 (natural units).
            omega (float): Angular frequency ω. Default is 1.0 (natural units).
            hbar (float): Reduced Planck constant ℏ. Default is 1.0 (natural
                units). Pass `scipy.constants.hbar` for SI calculations.

        Raises:
            ValueError: If mass, omega, or hbar are not strictly positive.
        """
        if mass <= 0:
            raise ValueError(f"mass must be positive, got {mass}")
        if omega <= 0:
            raise ValueError(f"omega must be positive, got {omega}")
        if hbar <= 0:
            raise ValueError(f"hbar must be positive, got {hbar}")

        self.mass = mass
        self.omega = omega
        self.hbar = hbar

        # The characteristic length scale of the oscillator.
        # Physically: x_0 = sqrt(ℏ / mω) sets the spatial extent
        # of the ground-state wavefunction (classical turning point ~ x_0).
        self._x0: float = math.sqrt(self.hbar / (self.mass * self.omega))

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def wavefunction(self, n: int, x: np.ndarray) -> np.ndarray:
        """
        Computes the nth energy eigenstate wavefunction ψ_n(x).

        Uses the analytic form:
            ψ_n(x) = N_n · H_n(ξ) · exp(-ξ²/2)
        where ξ = x/x_0 is the dimensionless coordinate and
        N_n = 1/sqrt(2ⁿ·n!·x_0·sqrt(π)) is the normalization constant.

        Args:
            n (int): Principal quantum number (n ≥ 0).
            x (np.ndarray): Position array over which to evaluate ψ_n.

        Returns:
            np.ndarray: The wavefunction values ψ_n(x), same shape as `x`.

        Raises:
            ValueError: If `n` is negative.
        """
        if n < 0:
            raise ValueError(f"Quantum number n must be >= 0, got {n}")

        xi = x / self._x0  # dimensionless coordinate ξ

        # Normalization constant N_n
        norm = 1.0 / math.sqrt(
            (2**n) * math.factorial(n) * self._x0 * math.sqrt(math.pi)
        )

        # scipy.special.hermite(n) returns a polynomial object callable on arrays
        H_n = hermite(n)

        psi: np.ndarray = norm * H_n(xi) * np.exp(-0.5 * xi**2)
        return psi

    def probability_density(self, n: int, x: np.ndarray) -> np.ndarray:
        """
        Computes the probability density |ψ_n(x)|² for the nth eigenstate.

        |ψ_n(x)|² dx gives the probability of finding the particle in the
        interval [x, x+dx]. The integral over all space equals 1 by construction.

        Args:
            n (int): Principal quantum number (n ≥ 0).
            x (np.ndarray): Position array.

        Returns:
            np.ndarray: The probability density |ψ_n(x)|², same shape as `x`.
        """
        psi = self.wavefunction(n, x)
        return psi**2  # Wavefunction is real for the QHO, so |ψ|² = ψ²

    def energy_level(self, n: int) -> float:
        """
        Returns the exact energy eigenvalue E_n for the nth eigenstate.

        The quantization rule E_n = (n + 1/2)ℏω is a direct consequence
        of the commutation relation [x̂, p̂] = iℏ. The 1/2 term represents
        the irreducible zero-point energy.

        Args:
            n (int): Principal quantum number (n ≥ 0).

        Returns:
            float: Energy eigenvalue E_n in the same units as ℏ·ω.

        Raises:
            ValueError: If `n` is negative.
        """
        if n < 0:
            raise ValueError(f"Quantum number n must be >= 0, got {n}")
        return (n + 0.5) * self.hbar * self.omega

    def classical_turning_point(self, n: int) -> float:
        """
        Returns the classical turning point x_tp for the nth eigenstate.

        At x_tp, the total energy equals the potential energy V(x_tp) = E_n,
        leaving zero kinetic energy — a particle here would stop and reverse
        classically. Quantum mechanically, tunneling allows |ψ_n|² to be
        non-zero beyond this point.

        Args:
            n (int): Principal quantum number (n ≥ 0).

        Returns:
            float: The positive turning point x_tp (the negative is -x_tp).
        """
        E_n = self.energy_level(n)
        # From (1/2)mω²x_tp² = E_n  =>  x_tp = sqrt(2*E_n / (mω²))
        x_tp: float = math.sqrt(2.0 * E_n / (self.mass * self.omega**2))
        return x_tp