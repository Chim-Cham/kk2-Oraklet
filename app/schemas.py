from pydantic import BaseModel

class DatasetStats(BaseModel):
    filename: str
    rows: int
    columns: int
    summary: str
    