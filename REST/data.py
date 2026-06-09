import pandas as pd
import uuid

def read_dataframe(df: pd.DataFrame):
    return {
        "id:": str(uuid.uuid4()),
        "rows": len(df),
        "columns": len(df.columns),
        "data_types": df.dtypes.astype(str).to_dict()
    }