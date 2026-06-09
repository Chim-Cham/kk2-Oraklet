import pandas as pd
import uuid
import shutil
import os

def read_dataframe(file):
    if not os.path.exists("uploads"):
        os.mkdir("uploads")
    dataset_id = str(uuid.uuid4())
    filepath = f"uploads/{dataset_id}.csv"
    print(f"Saving to: {filepath}")
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file, buffer)
    print(f"Reading from: {filepath}")
    df = pd.read_csv(filepath)

    return {
        "id:": dataset_id,
        "rows": len(df),
        "columns": len(df.columns),
        "data_types": df.dtypes.astype(str).to_dict()
    }