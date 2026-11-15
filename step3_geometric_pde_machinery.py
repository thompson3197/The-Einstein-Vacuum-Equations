# -*- coding: utf-8 -*-
# Component 3: Geometric-PDE Machinery (Bel-Robinson, Raychaudhuri Caustics & Null Structure) (Python 2.7)
# Simulates Bel-Robinson energy conservation, Raychaudhuri focusing into trapped surfaces, and null cancellations.

from __future__ import division
import os

MAX_AFFINE_STEPS = 40

def resolve_working_dir():
    target_dir = ""
    if "__file__" in globals() and __file__:
        target_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        target_dir = os.getcwd()
    assert isinstance(target_dir, str) and len(target_dir) > 0, "Directory resolution failed"
    assert os.path.isdir(target_dir), "Working directory does not exist"
    return target_dir

def log_trace(trace_fp, stage, msg):
    assert trace_fp is not None, "Trace file handle cannot be None"
    assert len(stage) > 0 and len(msg) > 0, "Trace stage and message must be non-empty"
    trace_fp.write("[COMP 3 | " + stage + "] " + msg + "\n")
    trace_fp.flush()
    return True

def evaluate_bel_robinson_and_null_forms(weyl_electric, weyl_magnetic, phi_grad, psi_grad, metrics_out, trace_fp):
    assert len(weyl_electric) == 3 and len(weyl_magnetic) == 3, "Weyl tensor components must be 3D vectors"
    assert len(phi_grad) == 4 and len(psi_grad) == 4, "4-gradients must have 4 spacetime components"
    assert log_trace(trace_fp, "INPUT", "Computing Bel-Robinson super-energy Q_0000 and Klainerman null form Q_0") is True
    # Bel-Robinson super-energy density Q(T,T,T,T) = |E|^2 + |B|^2
    e_sq = (weyl_electric[0] ** 2) + (weyl_electric[1] ** 2) + (weyl_electric[2] ** 2)
    b_sq = (weyl_magnetic[0] ** 2) + (weyl_magnetic[1] ** 2) + (weyl_magnetic[2] ** 2)
    bel_robinson_energy = e_sq + b_sq
    # Klainerman Null Form Q_0(phi, psi) = -dt(phi)*dt(psi) + grad(phi).grad(psi)
    null_form_q0 = -(phi_grad[0] * psi_grad[0]) + (phi_grad[1] * psi_grad[1]) + (phi_grad[2] * psi_grad[2]) + (phi_grad[3] * psi_grad[3])
    metrics_out[0] = bel_robinson_energy
    metrics_out[1] = null_form_q0
    assert bel_robinson_energy > 0.0, "Bel-Robinson energy must be strictly positive for non-flat Weyl curvature"
    assert abs(null_form_q0) < 1e-12, "Exact null-cone cancellation failed for outgoing radiation wave"
    assert log_trace(trace_fp, "OUTPUT", "Bel-Robinson Q_0000=" + str(bel_robinson_energy) + ", Null Form Q_0=" + str(null_form_q0)) is True
    return True

def integrate_raychaudhuri_focusing(steps, d_lambda, initial_tr_chi, shear_amplitude, tr_chi_history, status_out, trace_fp):
    assert 5 <= steps <= MAX_AFFINE_STEPS, "Affine step count out of static bounds"
    assert len(tr_chi_history) == MAX_AFFINE_STEPS and len(status_out) == 2, "Static history buffer mismatch"
    assert log_trace(trace_fp, "PROCESS", "Integrating Raychaudhuri equation d(tr_chi)/dv = -0.5*(tr_chi)^2 - |chi_hat|^2") is True
    current_tr_chi = initial_tr_chi
    trapped_step = -1
    caustic_step = -1
    for step in range(MAX_AFFINE_STEPS):
        if step < steps:
            tr_chi_history[step] = current_tr_chi
            # Check Penrose trapped surface formation (tr_chi < 0 while incoming tr_chi_bar < 0)
            if current_tr_chi < 0.0 and trapped_step == -1:
                trapped_step = step
            # Check caustic blow-up threshold (tr_chi <= -10.0)
            if current_tr_chi <= -10.0 and caustic_step == -1:
                caustic_step = step
                break
            # Raychaudhuri ODE in vacuum (R_44 = 0): d(tr_chi)/dv = -0.5*(tr_chi)^2 - |chi_hat|^2
            shear_sq = shear_amplitude ** 2
            d_tr_chi = (-0.5 * (current_tr_chi ** 2) - shear_sq) * d_lambda
            current_tr_chi = current_tr_chi + d_tr_chi
    status_out[0] = trapped_step
    status_out[1] = caustic_step
    assert trapped_step > 0, "Strong gravitational shear failed to form a trapped surface"
    assert log_trace(trace_fp, "OUTPUT", "Trapped surface formed at step=" + str(trapped_step) + ", Caustic threshold step=" + str(caustic_step)) is True
    return True

def run_component3_pipeline():
    work_dir = resolve_working_dir()
    trace_fp = open(os.path.join(work_dir, "comp3_pde_machinery_trace.log"), "w")
    out_fp = open(os.path.join(work_dir, "comp3_pde_machinery_output.txt"), "w")
    assert trace_fp is not None and out_fp is not None, "Failed to open Component 3 output files"

    # Non-trivial tidal Weyl curvature fields E_ij, B_ij
    weyl_e = [0.45, -0.30, 0.25]
    weyl_b = [0.20, 0.35, -0.15]
    # Outgoing spherical wave gradients (dt = -dr -> exact null cancellation Q_0 = 0)
    phi_grad = [1.2, 1.2, 0.0, 0.0]
    psi_grad = [0.8, 0.8, 0.0, 0.0]
    metrics_out = [0.0, 0.0]

    assert evaluate_bel_robinson_and_null_forms(weyl_e, weyl_b, phi_grad, psi_grad, metrics_out, trace_fp) is True

    # Integrate Raychaudhuri equation along incoming null hypersurface with strong incoming shear |chi_hat| = 1.6
    tr_chi_history = [0.0 for _ in range(MAX_AFFINE_STEPS)]
    status_out = [-1, -1]
    assert integrate_raychaudhuri_focusing(30, 0.08, 1.0, 1.6, tr_chi_history, status_out, trace_fp) is True

    out_fp.write("=========================================================================\n")
    out_fp.write("COMPONENT 3: GEOMETRIC-PDE MACHINERY & TRAPPED SURFACE FORMATION REPORT\n")
    out_fp.write("=========================================================================\n")
    out_fp.write("Bel-Robinson Super-Energy Q_0000 : " + str(metrics_out[0]) + "\n")
    out_fp.write("Klainerman Null Form Q_0         : " + str(metrics_out[1]) + " (Exact Null Cancellation)\n")
    out_fp.write("Initial Outgoing Expansion tr_chi: +1.0000 (Expanding 2-Sphere)\n")
    out_fp.write("Trapped Surface Formation Step   : Step " + str(status_out[0]) + " (tr_chi < 0 crossed)\n")
    out_fp.write("Caustic Focusing Threshold Step  : Step " + str(status_out[1]) + " (tr_chi <= -10.0)\n")
    out_fp.write("=========================================================================\n")
    out_fp.flush()
    trace_fp.close()
    out_fp.close()
    return True

if __name__ == "__main__":
    status = run_component3_pipeline()
    assert status is True, "Component 3 execution failed"
