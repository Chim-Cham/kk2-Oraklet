from transformers import pipeline
from .runnable import Runnable
import re
from app.schemas import DatasetQuestion, DatasetContext
from app.data import max_row, min_row, average_number, count_rows, count_columns, find_identifier

pipe = pipeline(
    "text-generation",
    model="HuggingFaceTB/SmolLM2-135M-Instruct",
    max_new_tokens=300,
    temperature=0,
)

OPERATIONS = {
    "highest": "max",
    "oldest": "max",
    "maximum": "max",
    "lowest": "min",
    "youngest": "min",
    "minimum": "min",
    "average": "average",
    "row" : "rows",
    "rows" : "rows",
    "column" : "columns",
    "columns" : "columns"
}

class ContextBuilder(Runnable[DatasetQuestion, DatasetContext]):

    def invoke(self, data: DatasetQuestion) -> DatasetContext:
        df = data.df
        question = data.question.lower()

        # Default response incase the given prompt can't be resolved.
        context = "Could not form a proper answer."       
        
        for keyword, operation in OPERATIONS.items():
            
            if keyword not in question:
                continue
            elif operation == "rows":
                return DatasetContext(
                    context=f"Number of Rows: {count_rows(df)}",
                    question=data.question
                )
            elif operation == "columns":
                return DatasetContext(
                    context=f"Number of Columns: {count_columns(df)}",
                    question=data.question
                )

            for col in df.select_dtypes(include="number").columns:
                
                if col.lower() in question:
                    if operation == "max":
                        
                        row = max_row(df, col)
                        identifier = find_identifier(df)

                        if identifier:
                            context = (
                                f"{identifier}: {row[identifier]}\n"
                                f"{col}: {row[col]}"
                            )
                        else:
                            context = row.to_string()
                            
                    elif operation == "min":
                        
                        row = min_row(df, col)
                        identifier = find_identifier(df)

                        if identifier:
                            context = (
                                f"{identifier}: {row[identifier]}\n"
                                f"{col}: {row[col]}"
                            )
                        else:
                            context = row.to_string()

                    elif operation == "average":
                        value = average_number(df[col])
                        context = f"{keyword.title()} {df[col]}: {value}"

                    break
                    

        return DatasetContext(
            context=context,
            question=data.question
        )


class PromptBuilder(Runnable[DatasetContext, str]):
    def invoke(self, data: DatasetContext):
        
        return f"""
            You're a helpful assistant.

            Rewrite this fact as one short sentence trying to answer the question.

            Do not take information from anywhere outside of this prompt.

            Information:
            {data.context}

            Question:
            {data.question}

            Sentence:
            """


class LLMRunner(Runnable[str, dict]):

    model_name: str = "HuggingFaceTB/SmolLM2-135M-Instruct"

    
    def invoke(self, prompt: str):

        result = pipe(
            prompt,
            max_new_tokens=200,
            temperature=0.1,
            return_full_text=False
        )

        return {
            "prompt": prompt,
            "response": result[0]["generated_text"],
            "model": self.model_name
        }


class ResponeParser(Runnable[str, dict]):
    def invoke(self, data: dict):

        answer = data["response"].strip()

        answer = answer.split("\n")[0].strip()
        """ answer = answer.strip("1. ") """
        answer = re.sub(r"^\d+\.\s*", "", answer)

        question = (
            data["prompt"].split("Question:")[-1].split("Sentence:")[0].strip()
        )

        return {
            "Question": question,
            "Answer": answer,
            "Model": data["model"]
        }