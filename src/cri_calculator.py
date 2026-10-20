
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "data" / "processed" / "session_features.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "cri_results.csv"

# PROVISIONAL ENGINEERING SETTINGS — NOT CLINICAL NORMS.
# Review and validate these values before interpreting participant scores.
PHYSIOLOGY_WEIGHT = 0.50
COGNITION_WEIGHT = 0.50

# Temporary mapping ranges for prototype testing.
RMSSD_RANGE_MS = (20.0, 70.0)
SDNN_RANGE_MS = (20.0, 70.0)
RT_RANGE_MS = (250.0, 800.0)


def bounded_score(value, low, high):
    """Map a numeric value to 0–100, clipping outside the range."""
    if pd.isna(value) or high <= low:
        return np.nan

    return float(np.clip((value - low) / (high - low) * 100, 0, 100))


def mean_available(values):
    """Average available numeric scores; return NaN if none are valid."""
    valid = [v for v in values if pd.notna(v)]
    return float(np.mean(valid)) if valid else np.nan


def calculate_row(row):
    # Physiological component:
    # Uses interval-derived variability features only.
    # GSR and movement are retained as separate indicators because
    # their interpretation depends on context and signal quality.
    rmssd_score = bounded_score(
        row.get("rmssd_ms", np.nan), *RMSSD_RANGE_MS
    )
    sdnn_score = bounded_score(
        row.get("sdnn_ms", np.nan), *SDNN_RANGE_MS
    )

    physiology_score = mean_available([rmssd_score, sdnn_score])

    # Cognitive component:
    # Accuracy is already expressed as a percentage by feature_extraction.py.
    accuracy = pd.to_numeric(
        pd.Series([row.get("nback_accuracy_pct", np.nan)]),
        errors="coerce",
    ).iloc[0]
    rt = pd.to_numeric(
        pd.Series([row.get("nback_median_rt_ms", np.nan)]),
        errors="coerce",
    ).iloc[0]

    # Do not assign a cognitive score unless both measurements exist.
    accuracy_score = (
        float(np.clip(accuracy, 0, 100))
        if pd.notna(accuracy)
        else np.nan
    )
    rt_score = (
        bounded_score(rt, *RT_RANGE_MS)
        if pd.notna(rt) and rt > 0
        else np.nan
    )

    cognition_score = (
        0.70 * accuracy_score + 0.30 * rt_score
        if pd.notna(accuracy_score) and pd.notna(rt_score)
        else np.nan
    )

    # Report the combined score only when both components are available.
    # This avoids silently treating missing physiology or cognition as zero.
    cri = (
        PHYSIOLOGY_WEIGHT * physiology_score
        + COGNITION_WEIGHT * cognition_score
        if pd.notna(physiology_score) and pd.notna(cognition_score)
        else np.nan
    )

    return pd.Series({
        "physiology_score_experimental": physiology_score,
        "cognitive_score_experimental": cognition_score,
        "cri_experimental": cri,
        "rmssd_score_experimental": rmssd_score,
        "sdnn_score_experimental": sdnn_score,
        "accuracy_score": accuracy_score,
        "reaction_time_score_experimental": rt_score,
        "gsr_mean_raw": row.get("gsr_mean_raw", np.nan),
        "gsr_unit": row.get("gsr_unit", ""),
        "accel_dynamic_rms_g": row.get("accel_dynamic_rms_g", np.nan),
        "signal_quality_mean": row.get("signal_quality_mean", np.nan),
        "score_status": "Experimental; requires validation",
    })


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Feature file not found: {INPUT_FILE}\n"
            "Run src/feature_extraction.py first."
        )

    features = pd.read_csv(INPUT_FILE)

    if features.empty:
        # Preserve an output file with the expected columns even before
        # participant data have been collected.
        result_columns = [
            "participant_id", "session_date", "intervention_day", "phase",
            "physiology_score_experimental",
            "cognitive_score_experimental", "cri_experimental",
            "rmssd_score_experimental", "sdnn_score_experimental",
            "accuracy_score", "reaction_time_score_experimental",
            "gsr_mean_raw", "gsr_unit", "accel_dynamic_rms_g",
            "signal_quality_mean", "score_status",
        ]
        results = pd.DataFrame(columns=result_columns)
    else:
        results = features.copy()

        scores = results.apply(calculate_row, axis=1)
        results = pd.concat([results, scores], axis=1)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_FILE, index=False)

    print(f"CRI calculation complete: {OUTPUT_FILE}")
    print(f"Session rows processed: {len(results)}")

    if results.empty:
        print("No participant data yet; output contains column headers only.")
    else:
        print(
            "Rows with a calculated CRI:",
            int(results["cri_experimental"].notna().sum()),
        )
        print("Scores are experimental, not clinically validated.")


if __name__ == "__main__":
    main()
