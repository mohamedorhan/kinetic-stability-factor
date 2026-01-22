#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kinetic Conversion Efficiency (S)
=================================

Author: Mohamed Orhan Zeinel
Email: mohamedorhanzeinel@gmail.com
ORCID: https://orcid.org/0009-0008-1139-8102
GitHub: https://github.com/mohamedorhan/kinetic-stability-factor
DOI (Zenodo): https://doi.org/10.5281/zenodo.11467499

Description
-----------
This module implements a reproducible digital-twin simulation for the
Kinetic Conversion Efficiency (S), defined as:

    S = Δv / ΔE

where:
    Δv : change in velocity (m/s or abstract proxy units)
    ΔE : total consumed energy (Joules)

IMPORTANT:
- This metric is NOT a physical law.
- It is a comparative efficiency metric under controlled conditions.
- Velocity for non-physical systems is treated as an abstract progress proxy.

License
-------
MIT License (recommended for open scientific reproducibility)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
import math
import random

# ============================================================
# Configuration
# ============================================================

RANDOM_SEED = 42
ENERGY_QUANTUM = 5.0  # Joules per step
random.seed(RANDOM_SEED)


# ============================================================
# Core Data Structures
# ============================================================

@dataclass(frozen=True)
class SystemParameters:
    """
    Immutable parameters defining a dynamic system.
    """
    name: str
    mass: float        # kg
    efficiency: float  # 0 < η ≤ 1
    energy_budget: float  # Joules
    abstract: bool = False  # True for non-physical systems


@dataclass
class SystemState:
    """
    Runtime state of a dynamic system.
    """
    velocity: float = 0.0
    energy_consumed: float = 0.0


# ============================================================
# Core Physics / Metric Logic
# ============================================================

def apply_energy_step(
    state: SystemState,
    params: SystemParameters,
    energy_step: float
) -> None:
    """
    Applies a discrete energy quantum to the system state.

    Uses the Work–Energy Theorem:
        ΔK = η · ΔE
        v_new = sqrt(v_old^2 + 2·ΔK / m)

    For abstract systems, velocity is interpreted as a
    normalized progress-rate proxy.
    """
    if state.energy_consumed >= params.energy_budget:
        return

    usable_energy = params.efficiency * energy_step
    delta_v_squared = (2.0 * usable_energy) / params.mass
    state.velocity = math.sqrt(state.velocity**2 + delta_v_squared)
    state.energy_consumed += energy_step


def kinetic_conversion_efficiency(state: SystemState) -> float:
    """
    Computes the Kinetic Conversion Efficiency S.

    Returns:
        S = Δv / ΔE
    """
    if state.energy_consumed <= 0.0:
        return 0.0
    return state.velocity / state.energy_consumed


# ============================================================
# Digital Twin Simulation
# ============================================================

def simulate_system(params: SystemParameters) -> Dict[str, float]:
    """
    Runs a full energy-budget simulation for a single system.
    """
    state = SystemState()

    while state.energy_consumed < params.energy_budget:
        apply_energy_step(state, params, ENERGY_QUANTUM)

    return {
        "system": params.name,
        "final_velocity": state.velocity,
        "energy_consumed": state.energy_consumed,
        "S": kinetic_conversion_efficiency(state),
        "abstract": params.abstract
    }


def run_experiment(systems: List[SystemParameters]) -> List[Dict[str, float]]:
    """
    Runs the digital twin experiment for multiple systems.
    """
    results = []
    for system in systems:
        results.append(simulate_system(system))
    return sorted(results, key=lambda x: x["S"], reverse=True)


# ============================================================
# Reproducible Benchmark Setup
# ============================================================

def benchmark_suite() -> List[SystemParameters]:
    """
    Defines standardized system archetypes.
    """
    return [
        SystemParameters(
            name="Agile Robot",
            mass=0.5,
            efficiency=0.70,
            energy_budget=60.0,
            abstract=False
        ),
        SystemParameters(
            name="Electric Vehicle",
            mass=1.0,
            efficiency=0.80,
            energy_budget=100.0,
            abstract=False
        ),
        SystemParameters(
            name="AI Agent (Abstract)",
            mass=1.0,
            efficiency=0.50,
            energy_budget=50.0,
            abstract=True
        ),
    ]


# ============================================================
# CLI Entry Point
# ============================================================

def main() -> None:
    """
    Main execution entry point.
    """
    systems = benchmark_suite()
    results = run_experiment(systems)

    print("\n=== Kinetic Conversion Efficiency Benchmark ===\n")
    for r in results:
        print(f"System           : {r['system']}")
        print(f"Final Velocity   : {r['final_velocity']:.6f}")
        print(f"Energy Consumed  : {r['energy_consumed']:.2f} J")
        print(f"S (Δv / ΔE)      : {r['S']:.6e}")
        print(f"Abstract System  : {r['abstract']}")
        print("-" * 50)


if __name__ == "__main__":
    main()
