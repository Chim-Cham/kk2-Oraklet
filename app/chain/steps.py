from transformers import pipeline
from .runnable import Runnable
from app.schemas import DatasetQuestion

pipe = pipeline(
    "text-generation",
    model="HuggingFaceTB/SmolLM2-135M-Instruct",
)

class PromptBuilder(Runnable[DatasetQuestion, str]):
    def invoke(self, data: DatasetQuestion) -> str:
        dataset = data.df.head(10).to_string(index=False)

        return f"""
            You are a helpful data analyst.

            The table below contains data.

            Answer ONLY the user's question.
            Do not repeat the dataset.
            Be concise.

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
            max_new_tokens=200,
            do_sample=False
        )

        return {
            "prompt": prompt,
            "response": result[0]["generated_text"],
            "model": self.model_name
        }


class ResponeParser(Runnable[str, dict]):
    def invoke(self, data: dict):

        answer = data["response"]
        
        if "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()
        
        question = ""

        if "Question:" in data["prompt"]:
            question = (
                data["prompt"].split("Question:")[-1].split("Answer:")[0].strip()
            )

        return {
            "question": question,
            "answer": answer,
            "model": data["model"]
        }