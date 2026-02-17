"""Load YOUR real filtered_complaints.csv"""
import pandas as pd
from .task2_config import DATA_PATH


def load_real_data():
    """Load your ACTUAL filtered complaints from Task 1"""
    print(f"📂 Loading YOUR real data: {DATA_PATH}")

    # Load with error handling
    try:
        df = pd.read_csv(DATA_PATH)
        print(f"✅ Loaded {len(df):,} complaints")
        print(f"📋 Columns: {df.columns.tolist()}")
        return df
    except Exception as e:
        print(f"❌ Error loading: {e}")
        # Try alternative encoding
        try:
            df = pd.read_csv(DATA_PATH, encoding="latin1")
            print(f"✅ Loaded with latin1 encoding: {len(df):,} complaints")
            print(f"📋 Columns: {df.columns.tolist()}")
            return df
        except:
            # Try with no headers assumption
            df = pd.read_csv(DATA_PATH, header=0)
            print(f"✅ Loaded with default settings: {len(df):,} complaints")
            print(f"📋 Columns: {df.columns.tolist()}")
            return df
