import pandas as pd
from src.config import DATA_PATH, CSV_FILES


def load_raw_data() -> dict[str, pd.DataFrame]:
    """Load every raw CSV and return a dict keyed by table name."""
    dfs = {}
    for name, filename in CSV_FILES.items():
        path = DATA_PATH / filename
        dfs[name] = pd.read_csv(path)
        print(f"  [load] {name:12s}: {dfs[name].shape}")
    return dfs
