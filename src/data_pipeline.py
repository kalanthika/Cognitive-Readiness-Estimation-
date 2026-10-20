
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def inspect_csv(filename, required_columns):
    """Load a CSV and report basic data-quality issues."""
    path = DATA_DIR / filename

    if not path.exists():
        print(f"\n[NOT FOUND] {path}")
        return None

    try:
        df = pd.read_csv(path)
    except Exception as exc:
        print(f"\n[READ ERROR] {filename}: {exc}")
        return None

    print(f"\n{'=' * 50}")
    print(f"File: {filename}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print(f"[WARNING] Missing columns: {missing_columns}")
    else:
        print("[OK] Required columns are present")

    print("\nMissing values per column:")
    print(df.isna().sum().to_string())

    if "timestamp" in df.columns:
        parsed = pd.to_datetime(df["timestamp"], errors="coerce")
        invalid_count = int(parsed.isna().sum())
        print(f"\nInvalid/missing timestamps: {invalid_count}")

    return df


def main():
    inspect_csv(
        "sessions.csv",
        [
            "participant_id",
            "session_date",
            "intervention_day",
            "phase",
        ],
    )

    inspect_csv(
        "sensor_readings.csv",
        [
            "participant_id",
            "timestamp",
            "heart_rate_bpm",
            "gsr_value",
        ],
    )

    inspect_csv(
        "cognitive_trials.csv",
        [
            "participant_id",
            "trial_number",
            "is_target",
            "response_made",
            "correct",
            "reaction_time_ms",
        ],
    )


if __name__ == "__main__":
    main()
