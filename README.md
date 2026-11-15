# Deterministic Verification Suite for Low-Regularity Einstein Vacuum Spacetimes ($R_{\mu\nu} = 0$)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/release/python-2718/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

This repository contains the standalone, deterministic computational verification engine accompanying the research proposal:

> **"Global Stability, Caustic Control, and Deterministic Verification of Low-Regularity Einstein Vacuum Spacetimes at the Scaling-Critical Sobolev Threshold"**

The software suite translates core geometric partial differential equation (PDE) estimatesâ€”spanning Einstein constraint residuals, scaling-critical Sobolev regularity regimes ($s_c = 3/2$), weak null condition energy growth, rough eikonal transport bounds, and coupled Bianchi-connection bootstrap closuresâ€”into auditable, zero-dependency Python 2.7 verification modules.

---

## Repository Architecture

```text
einstein-vacuum-low-regularity/
â”œâ”€â”€ README.md                                  # Repository documentation & execution guide
â”œâ”€â”€ LICENSE                                    # Open-source MIT license
â”œâ”€â”€ CITATION.cff                               # Standard academic software citation metadata
â”œâ”€â”€ .zenodo.json                               # Zenodo archival & indexing metadata
â”œâ”€â”€ step1_einstein_constraints_adm.py          # Component 1: Hamiltonian/Momentum constraints & ADM mass
â”œâ”€â”€ step2_regularity_gauge_analyzer.py         # Component 2: Sobolev scaling thresholds & gauge classifier
â”œâ”€â”€ step3_geometric_pde_machinery.py           # Component 3: Bel-Robinson energy & Raychaudhuri caustics
â”œâ”€â”€ task1_weak_null_stability.py               # Task 1: Weak null condition bootstrap energy solver
â”œâ”€â”€ task2_eikonal_rough_estimates.py           # Task 2: Rough eikonal & null connection bounds
â”œâ”€â”€ task3_bianchi_connection_coupling.py       # Task 3: Coupled Bianchi-connection bootstrap closure
â””â”€â”€ einstein_unified_research_system.py        # Unified master verification controller
```

---

## Safety-Critical & Deterministic Engineering Standards

To guarantee 100% reproducibility across workstations, grant review panels, and archival environments, every module strictly enforces the following engineering invariants:

1. **Zero External Dependencies:** Uses only the Python 2.7 standard library (`__future__`, `os`, `math`).
2. **Static Memory Allocation:** All spatial shells, metric tensors, curvature flux histories, and null expansion arrays are pre-allocated within fixed upper bounds (`MAX_GRID`, `MAX_DIM`, `MAX_SLABS`, `MAX_TIME_STEPS`) at startup.
3. **Assertion-First Mathematical Verification:** Every subroutine validates mathematical invariants (e.g., Positive Mass Theorem $M_{\mathrm{ADM}} \ge 0$, exact null-form cancellation $Q_0 = 0$, and Sobolev bootstrap caps) via dual `assert` guards.
4. **Automated Input/Process/Output Traceability:** Executing any script automatically resolves the local working directory (`os.getcwd()`) and writes structured execution traces (`*.log`) alongside formal verification certificates (`*.txt`).

---

## Quickstart & Execution

### Prerequisites
* Python 2.7.x (tested on Python 2.7.13+)

### Running Individual Modules
Execute any standalone component directly from your IDE or terminal:

```bash
python step1_einstein_constraints_adm.py
python step2_regularity_gauge_analyzer.py
python step3_geometric_pde_machinery.py
python task1_weak_null_stability.py
python task2_eikonal_rough_estimates.py
python task3_bianchi_connection_coupling.py
```

### Running the Unified Master Verification System
To execute the end-to-end 3-node research verification pipeline and generate the master certificate:

```bash
python einstein_unified_research_system.py
```

Upon completion, verify that `einstein_unified_master_trace.log` and `einstein_unified_master_certificate.txt` appear in your working directory with `FINAL VERDICT : GLOBAL STABILITY & REGULARITY SYSTEM VERIFIED = TRUE`.

---

## Archival & Citation

When referencing this computational verification framework in grant proposals, preprints, or peer-reviewed publications, please cite the archived Zenodo release via the metadata in `CITATION.cff`.
