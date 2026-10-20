
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

SCHEMAS = {
    "sessions.csv": [
        "participant_id", "session_date", "intervention_day",
        "phase", "sleep_hours", "caffeine_amount_mg",
        "stress_self_report", "stress_scale",
    ],
    "sensor_readings.csv": [
        "participant_id", "session_date", "intervention_day",
        "phase", "timestamp", "heart_rate_bpm",
        "ppg_interval_ms", "gsr_value", "gsr_unit",
        "accel_x", "accel_y", "accel_z",
        "gyro_x", "gyro_y", "gyro_z", "imu_unit",
        "signal_quality",
    ],
    "cognitive_trials.csv": [
        "participant_id", "session_date", "intervention_day",
        "phase", "trial_number", "is_target",
        "response_made", "correct", "reaction_time_ms",
    ],
}


def inspect_csv(filename, required_columns):
    path = DATA_DIR / filename

    if not path.exists():
        print(f"\n[NOT FOUND] {path}")
        return

    try:
        df = pd.read_csv(path)
    except Exception as exc:
        print(f"\n[READ ERROR] {filename}: {exc}")
        return

    print(f"\n--- {filename} ---")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        print(f"[WARNING] Missing columns: {missing_columns}")
    else:
        print("[OK] Required columns are present")

    print("\nMissing values per column:")
    print(df.isna().sum().to_string())

    if "timestamp" in df.columns:
        parsed = pd.to_datetime(df["timestamp"], errors="coerce")
        print(
            "\nInvalid/missing timestamps:",
            int(parsed.isna().sum()),
        )


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Create empty templates only when files do not exist.
    for filename, columns in SCHEMAS.items():
        path = DATA_DIR / filename

        if not path.exists():
            pd.DataFrame(columns=columns).to_csv(path, index=False)
            print(f"[CREATED] {filename}")

    # Validate every template, including existing files.
    for filename, columns in SCHEMAS.items():
        inspect_csv(filename, columns)


if __name__ == "__main__":
    main()
