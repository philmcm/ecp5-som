import yaml
import pandas as pd
from types import SimpleNamespace

def load_config(yaml_file):
    with open(yaml_file, 'r') as f:
        return SimpleNamespace(**yaml.safe_load(f))

def process_data(path):
    return pd.read_csv(path, encoding='utf-8', header=None)

def trim_to_header(df, marker):
    start_index = df.apply(lambda row: row.astype(str).str.contains(marker).any(), axis=1).idxmax()
    df.columns = df.iloc[start_index]
    return df.iloc[start_index+1:].reset_index(drop=True)