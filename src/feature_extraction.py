
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = DATA_DIR / "processed"

KEYS = [
    "participant_id",
    "session_date",
    "intervention_day",
    "phase",
]

NUMERIC_SENSOR_COLUMNS = [
    "heart_rate_bpm", "ppg_interval_ms", "gsr_value",
    "accel_x", "accel_y", "accel_z",
    "gyro_x", "gyro_y", "gyro_z",
]

def load_csv(name):
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    return pd.read_csv(path)


def numeric(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def safe_mean(series):
    values = pd.to_numeric(series, errors="coerce").dropna()
    return float(values.mean()) if len(values) else np.nan


def interval_features(intervals):
    """Descriptive features from supplied pulse intervals; not ECG-validated HRV."""
    x = pd.to_numeric(intervals, errors="coerce").dropna()
    x = x[(x >= 300) & (x <= 2000)]

    result = {
        "interval_count": int(len(x)),
        "rmssd_ms": np.nan,
        "sdnn_ms": np.nan,
    }

    if len(x) >= 3:
        diffs = np.diff(x.to_numpy())
        result["rmssd_ms"] = float(np.sqrt(np.mean(diffs ** 2)))
        result["sdnn_ms"] = float(x.std(ddof=1))

    return result


def sensor_features(group):
    result = {
        "sensor_rows": int(len(group)),
        "hr_bpm_mean": np.nan,
        "interval_count": 0,
        "rmssd_ms": np.nan,
        "sdnn_ms": np.nan,
        "gsr_mean_raw": np.nan,
        "gsr_unit": "unknown",
        "gsr_peak_count_exploratory": np.nan,
        "accel_magnitude_mean_g": np.nan,
        "accel_dynamic_rms_g": np.nan,
        "gyro_magnitude_mean": np.nan,
        "signal_quality_mean": np.nan,
    }

    if "heart_rate_bpm" in group:
        hr = group["heart_rate_bpm"].dropna()
        hr = hr[(hr >= 30) & (hr <= 220)]
        result["hr_bpm_mean"] = safe_mean(hr)

    if "ppg_interval_ms" in group:
        result.update(interval_features(group["ppg_interval_ms"]))

    if "gsr_value" in group:
        gsr = group["gsr_value"].dropna()
        result["gsr_mean_raw"] = safe_mean(gsr)

        if "gsr_unit" in group and group["gsr_unit"].notna().any():
            result["gsr_unit"] = str(
                group["gsr_unit"].dropna().iloc[0]
            )

        # Exploratory local maxima only. This is NOT a validated SCR detector.
        if len(gsr) >= 5:
            values = gsr.to_numpy()
            peaks = (
                (values[1:-1] > values[:-2])
                & (values[1:-1] > values[2:])
            )
            result["gsr_peak_count_exploratory"] = int(peaks.sum())

    axes = ["accel_x", "accel_y", "accel_z"]
    if all(c in group.columns for c in axes):
        acc = group[axes].apply(pd.to_numeric, errors="coerce").dropna()
        if len(acc):
            magnitude = np.sqrt((acc ** 2).sum(axis=1))
            result["accel_magnitude_mean_g"] = float(magnitude.mean())

            # Removes each axis' window mean as a simple exploratory
            # dynamic-motion approximation; not a calibrated gravity filter.
            centered = acc - acc.mean()
            result["accel_dynamic_rms_g"] = float(
                np.sqrt(np.mean(centered.to_numpy() ** 2))
            )

    axes = ["gyro_x", "gyro_y", "gyro_z"]
    if all(c in group.columns for c in axes):
        gyro = group[axes].apply(pd.to_numeric, errors="coerce").dropna()
        if len(gyro):
            magnitude = np.sqrt((gyro ** 2).sum(axis=1))
            result["gyro_magnitude_mean"] = float(magnitude.mean())

    if "signal_quality" in group:
        quality = pd.to_numeric(group["signal_quality"], errors="coerce")
        result["signal_quality_mean"] = safe_mean(quality)

    return result


def cognitive_features(group):
    result = {
        "nback_trials": int(len(group)),
        "nback_hits": np.nan,
        "nback_misses": np.nan,
        "nback_false_alarms": np.nan,
        "nback_accuracy_pct": np.nan,
        "nback_median_rt_ms": np.nan,
    }

    for col in ["is_target", "response_made", "correct", "reaction_time_ms"]:
        if col in group:
            group[col] = pd.to_numeric(group[col], errors="coerce")

    if not {"is_target", "response_made"}.issubset(group.columns):
        return result

    valid = group.dropna(subset=["is_target", "response_made"]).copy()
    if valid.empty:
        return result

    target = valid["is_target"].astype(bool)
    response = valid["response_made"].astype(bool)

    hits = int((target & response).sum())
    misses = int((target & ~response).sum())
    false_alarms = int((~target & response).sum())

    result["nback_hits"] = hits
    result["nback_misses"] = misses
    result["nback_false_alarms"] = false_alarms

    if "correct" in valid:
        scored = valid["correct"].dropna()
        if len(scored):
            result["nback_accuracy_pct"] = float(scored.mean() * 100)
    else:
        result["nback_accuracy_pct"] = float(
            (target == response).mean() * 100
        )

    if "reaction_time_ms" in valid:
        rt = valid["reaction_time_ms"].dropna()
        rt = rt[(rt > 0) & (rt <= 10000)]
        if len(rt):
            result["nback_median_rt_ms"] = float(rt.median())

    return result


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sessions = load_csv("sessions.csv")
    sensors = numeric(load_csv("sensor_readings.csv"), NUMERIC_SENSOR_COLUMNS)
    trials = load_csv("cognitive_trials.csv")

    for name, df in [
        ("sessions.csv", sessions),
        ("sensor_readings.csv", sensors),
        ("cognitive_trials.csv", trials),
    ]:
        missing = [key for key in KEYS if key not in df.columns]
        if missing:
            raise ValueError(f"{name} is missing grouping columns: {missing}")

    session_keys = sessions[KEYS].drop_duplicates()

    if session_keys.empty:
        # Empty template: produce an empty output with useful headers.
        columns = KEYS + list(sensor_features(sensors.head(0)).keys())
        columns += list(cognitive_features(trials.head(0)).keys())
        output = pd.DataFrame(columns=list(dict.fromkeys(columns)))
    else:
        records = []

        for _, session in session_keys.iterrows():
            mask_s = pd.Series(True, index=sensors.index)
            mask_t = pd.Series(True, index=trials.index)

            for key in KEYS:
                mask_s &= sensors[key].eq(session[key])
                mask_t &= trials[key].eq(session[key])

            sensor_group = sensors.loc[mask_s]
            trial_group = trials.loc[mask_t]

            record = session.to_dict()
            record.update(sensor_features(sensor_group))
            record.update(cognitive_features(trial_group))
            records.append(record)

        output = pd.DataFrame(records)

    output_path = OUTPUT_DIR / "session_features.csv"
    output.to_csv(output_path, index=False)

    print(f"Feature extraction complete: {output_path}")
    print(f"Session rows: {len(output)}")
    print("Empty templates are expected to produce zero session rows.")
if __name__ == "__main__":
    main()