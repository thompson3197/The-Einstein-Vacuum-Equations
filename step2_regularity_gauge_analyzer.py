# -*- coding: utf-8 -*-
# Component 2: Sobolev Regularity Thresholds & Gauge Stability Classifier (Python 2.7)
# Evaluates scaling exponents s vs s_c = 1.5, curvature integrability, and optimal gauge selection.

from __future__ import division
import os

MAX_REGIMES = 8
CRITICAL_SOBOLEV_SC = 1.5

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
    trace_fp.write("[COMP 2 | " + stage + "] " + msg + "\n")
    trace_fp.flush()
    return True

def classify_regularity_regimes(s_values, count, scaling_weights, regime_labels, gauge_choices, trace_fp):
    assert 1 <= count <= MAX_REGIMES, "Regime count out of bounds"
    assert len(s_values) == MAX_REGIMES and len(scaling_weights) == MAX_REGIMES, "Static buffer mismatch"
    assert log_trace(trace_fp, "INPUT", "Evaluating " + str(count) + " Sobolev H^s regularity thresholds against s_c=1.5") is True
    for idx in range(MAX_REGIMES):
        if idx < count:
            s_exp = s_values[idx]
            # Scaling exponent = s_c - s = 1.5 - s (negative = subcritical, 0 = critical)
            scaling_weights[idx] = CRITICAL_SOBOLEV_SC - s_exp
            if s_exp > 2.5:
                regime_labels[idx] = "Classical Energy Regime (Lipschitz Metric)"
                gauge_choices[idx] = "Wave Coordinates (Box_g x^u = 0)"
            elif s_exp == 2.0:
                regime_labels[idx] = "L^2 Curvature Threshold (KRS 2015 Resolved)"
                gauge_choices[idx] = "Maximal Foliation + Double Null Parametrix"
            elif CRITICAL_SOBOLEV_SC < s_exp < 2.0:
                regime_labels[idx] = "Sub-Threshold Rough Data (Postdoc Frontier)"
                gauge_choices[idx] = "Double Null Foliation + Renormalized Ricci"
            elif s_exp == CRITICAL_SOBOLEV_SC:
                regime_labels[idx] = "Scale-Invariant Critical Space H^(3/2)"
                gauge_choices[idx] = "Characteristic Double Null / Scale-Critical"
            else:
                regime_labels[idx] = "Supercritical Ill-Posed Regime (Norm Inflation)"
                gauge_choices[idx] = "Breakdown / Trapped Caustic Singularity"
    assert log_trace(trace_fp, "OUTPUT", "Classified regularity regimes and gauge strategies cleanly") is True
    return True

def verify_lipschitz_embedding(s_values, count, lipschitz_flags, trace_fp):
    assert 1 <= count <= MAX_REGIMES, "Invalid count for embedding check"
    assert len(lipschitz_flags) == MAX_REGIMES, "Invalid lipschitz_flags buffer"
    assert log_trace(trace_fp, "PROCESS", "Checking 3D Sobolev embedding H^s(R^3) -> C^(0,1) (s > 5/2)") is True
    for idx in range(MAX_REGIMES):
        if idx < count:
            # In 3D, H^s embeds into Lipschitz C^(0,1) iff s > 3/2 + 1 = 2.5
            if s_values[idx] > 2.5:
                lipschitz_flags[idx] = 1
            else:
                lipschitz_flags[idx] = 0
    assert lipschitz_flags[0] == 1 and lipschitz_flags[3] == 0, "Sobolev embedding boundary logic failed"
    assert log_trace(trace_fp, "OUTPUT", "Verified classical Lipschitz breakdown below s = 2.5") is True
    return True

def run_component2_pipeline():
    work_dir = resolve_working_dir()
    trace_fp = open(os.path.join(work_dir, "comp2_regularity_trace.log"), "w")
    out_fp = open(os.path.join(work_dir, "comp2_regularity_output.txt"), "w")
    assert trace_fp is not None and out_fp is not None, "Failed to open Component 2 output files"

    s_values = [3.0, 2.51, 2.0, 1.75, 1.5, 1.25, 0.0, 0.0]
    scaling_weights = [0.0 for _ in range(MAX_REGIMES)]
    regime_labels = ["" for _ in range(MAX_REGIMES)]
    gauge_choices = ["" for _ in range(MAX_REGIMES)]
    lipschitz_flags = [0 for _ in range(MAX_REGIMES)]
    active_count = 6

    assert classify_regularity_regimes(s_values, active_count, scaling_weights, regime_labels, gauge_choices, trace_fp) is True
    assert verify_lipschitz_embedding(s_values, active_count, lipschitz_flags, trace_fp) is True

    out_fp.write("=================================================================================\n")
    out_fp.write("COMPONENT 2: SOBOLEV REGULARITY THRESHOLDS & GAUGE SELECTION REPORT (s_c = 1.5)\n")
    out_fp.write("=================================================================================\n")
    for idx in range(MAX_REGIMES):
        if idx < active_count:
            out_fp.write("H^" + str(s_values[idx]) + " | Scale_Exp=" + str(scaling_weights[idx]) +
                         " | Lipschitz=" + str(lipschitz_flags[idx]) +
                         " | " + regime_labels[idx] + " -> " + gauge_choices[idx] + "\n")
    out_fp.write("=================================================================================\n")
    out_fp.flush()
    trace_fp.close()
    out_fp.close()
    return True

if __name__ == "__main__":
    status = run_component2_pipeline()
    assert status is True, "Component 2 execution failed"
