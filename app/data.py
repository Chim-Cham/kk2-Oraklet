from io import BytesIO
import pandas as pd
from fastapi import HTTPException

_upLoadedFile = None
_fileName = None

# API Functions
def upload_file(filename: str, data: bytes):
    global _upLoadedFile, _fileName

    _upLoadedFile = BytesIO(data)
    _fileName = filename

def get_dataframe() -> pd.DataFrame:
    if _upLoadedFile is None:
        raise HTTPException(
            status_code=404,
            detail="No dataset found!"
        )

    _upLoadedFile.seek(0)

    return pd.read_csv(_upLoadedFile)

def get_filename() -> str:
    return _fileName

def data_stats():
    df = get_dataframe()
    return df.describe(include="all").fillna("").to_dict()

def data_stats_text():
    df = get_dataframe()
    return {
        "Rows": len(df),
        "Columns": list(df.columns),
        "Numeric": df.describe().round(2).to_dict(),
    }

# Pandas for data management
def max_row(df, column):
    return df.loc[df[column].idxmax()]

def min_row(df, column):
    return df.loc[df[column].idxmin()]

def count_rows(df):
    result = len(df)
    return result

def count_columns(df):
    result = len(df.columns)
    return result

def average_number(df):
    result = df.mean()
    return result

def find_identifier(df):
    for col in df.columns:
        if df[col].dtype == "object":
            return col
    return None