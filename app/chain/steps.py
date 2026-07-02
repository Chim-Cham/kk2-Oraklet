from transformers import pipeline
from .runnable import Runnable
from app.schemas import DatasetQuestion

pipe = pipeline(
    "text-generation",
    model="HuggingFaceTB/SmolLM2-135M-Instruct",
    max_new_tokens=300,
    temperature=0,
)

class PromptBuilder(Runnable[DatasetQuestion, str]):
    def invoke(self, data: DatasetQuestion) -> str:
        dataset = data.df.head(20).to_string(index=False)

        return f"""
            You are a helpful data analyst.

            Use ONLY the information in the dataset.

            Rules:
            - Answer the user's question.
            - Do not ask another question.
            - Do not repeat the dataset.
            - Respond with a single short answer.

            Dataset:
            {dataset}

            Question:
            {data.question}

            Answer:
            """




class LLMRunner(Runnable[str, dict]):

    model_name: str = "HuggingFaceTB/SmolLM2-135M-Instruct"

    
    def invoke(self, prompt: str):

        result = pipe(
            prompt,
            max_new_tokens=20,
            do_sample=False,
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
        
        question = (
            data["prompt"].split("Question:")[-1].split("Answer:")[0].strip()
        )

        return {
            "question": question,
            "answer": answer,
            "model": data["model"]
        }