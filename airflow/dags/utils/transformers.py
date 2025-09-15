import json
import pandas as pd
from shapely.geometry import Point

def to_upper(df: pd.DataFrame, cols: list[str]):
    df[cols] = df[cols].apply(lambda col: col.str.upper())

    return df

def to_normalized_date(df: pd.DataFrame, cols: list[str]):
    for col in cols:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

    return df

def to_geopoint(df: pd.DataFrame, cols: list[str]):
    for col in cols:
        df[col] = df[col].apply(lambda geo: Point(geo["lon"], geo["lat"]))

    return df

def to_json(df: pd.DataFrame, cols: list[str]):
    for col in cols:
        df[col] = df[col].apply(lambda col: json.dumps(col) if col is not None else None)

    return df

def drop(df: pd.DataFrame, cols: dict):
    df = df.drop(columns = cols)

    return df

# Always call rename as the last transformation in the chain!
def rename(df: pd.DataFrame, cols: dict):
    df = df.rename(columns = cols)

    return df