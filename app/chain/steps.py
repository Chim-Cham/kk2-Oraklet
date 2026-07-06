from transformers import pipeline
from .runnable import Runnable
from app.schemas import DatasetQuestion
from app.data import dataset_context, max_row, min_row, average_row

pipe = pipeline(
    "text-generation",
    model="HuggingFaceTB/SmolLM2-135M-Instruct",
    max_new_tokens=300,
    temperature=0,
)


class PromptBuilder(Runnable[DatasetQuestion, str]):
    def invoke(self, data: DatasetQuestion) -> str:
        
        context = dataset_context(data.df)

        return f"""
            You are a data analyst answering questions from a user.

            Rules:
            - Answer the user's question.
            - Do not ask another question.
            - Do not repeat the dataset.
            - Respond with a single short answer.
            - Use ONLY the information in the dataset.

            {context}

            Highest value for each column:
            {max_row}

            Lowest value for each column:
            {min_row}

            Average value for each column:
            {average_row}

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
            do_sample=False,
            return_full_text=False
        )

        print(result)

        return {
            "prompt": prompt,
            "response": result[0]["generated_text"],
            "model": self.model_name
        }


class ResponeParser(Runnable[str, dict]):
    def invoke(self, data: dict):

        print(data["response"])

        answer = data["response"].strip()

        answer = answer.split("\n")[0].strip()
        
        question = (
            data["prompt"].split("Question:")[-1].split("Answer:")[0].strip()
        )

        return {
            "Question": question,
            "Answer": answer,
            "Model": data["model"]
        }