
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Dataset inspection setup is ready.")
print(f"Project folder: {ROOT}")
print(f"Output folder: {OUTPUT_DIR}")

# Inspect your existing project CSV templates.
for filename in [
    "sessions.csv",
    "sensor_readings.csv",
    "cognitive_trials.csv",
]:
    path = ROOT / "data" / filename

    if path.exists():
        df = pd.read_csv(path)
        print(f"\n{filename}: {len(df)} rows")
        print("Columns:", df.columns.tolist())
    else:
        print(f"\nNot created yet: {path}")
