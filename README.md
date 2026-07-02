An asynchronous, event-driven 3D Kinetic Monte Carlo (KMC) simulation framework engineered to model vacancy-mediated atom migration kinetics in Face-Centered Cubic (FCC) crystalline lattices. This tool bridges atomic-scale stochastic jump mechanics with macroscopic thermodynamic transport metrics, enabling users to empirically extract vacancy migration energies ($E_m$) and visualize diffusion trajectories.

---

## 🚀 Features

- **3D FCC Kinetic Lattice Mapping:** Tracks a multi-dimensional grid simulating realistic physical crystal geometries (e.g., pure Aluminum).
- **Periodic Boundary Conditions (PBC):** Seamlessly handles coordinate mapping across edge constraints while maintaining an independent "unwrapped" coordinate system for displacement analysis.
- **Residence-Time Algorithm (BKL):** Implements the exact Bortz-Kalos-Lebowitz algorithm to advance a variable physical timeline based on exact escape probabilities rather than arbitrary fixed steps.
- **Isothermal Temperature Sweeps:** Automates execution across varying temperature states to perform Arrhenius regression analyses.
- **Unified Command-Line Interface (CLI):** Features a polished entry point to manage simulations, track trajectories, and generate figures natively.

---

## 📁 Repository Architecture

```text
Edge_FCC_Kinetics_Optimizer/
│
├── core_engine/
│   └── diffusion.py        # Core physics engine (FCC neighborhood mapping, KMC clocks)
│
├── analysis/
│   ├── run_diffusion_experiment.py  # Single-temperature long-trajectory tracking script
│   ├── plot_results.py              # Publication-grade MSD visualization handler
│   └── temperature_sweep.py         # Automated Arrhenius sweep and regression tool
│
├── data/                            # Auto-generated runtime data outputs
│   ├── experiment_results.csv       # Trajectory tracking dataset
│   ├── msd_vs_time.png              # Mean Squared Displacement trajectory graph
│   ├── arrhenius_sweep_results.csv  # Temperature sweep metric table
│   └── arrhenius_plot.png           # Finished Arrhenius slope fit visualization
│
├── main.py                          # Unified CLI Application Entry Point
├── README.md                        # Framework Documentation
└── dev-setup.md                     # Developer environment setup configurations