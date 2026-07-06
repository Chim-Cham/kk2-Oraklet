from pydantic import BaseModel
import pandas as pd

class QuestionRequest(BaseModel):
    question: str
    
class QuestionResponse(BaseModel):
    answer: str

class DatasetQuestion(BaseModel):
    df: pd.DataFrame

    model_config = {
        'arbitrary_types_allowed': True
    }

    question: str

class DatasetContext(BaseModel):
    context: str
    question: str