from transformers import pipeline
from .runnable import Runnable

pipe = pipeline(
    "text-generation",
    model="HuggingFaceTB/SmolLM2-135M-Instruct",
)

class PromptBuilder(Runnable[dict, str]):
    def invoke(self, data: dict):
        dataset = data["df"].to_string(index=False)

        return f"""
            Dataset:

            {dataset}

            Question:
            {data["question"]}

            Answer:
            """




class LLMRunner(Runnable[str, str]):
    def invoke(self, prompt: str):

        result = pipe(
            prompt,
            max_new_tokens=200,
            do_sample=False
        )

        return result[0]["generated_text"]



class ResponeParser(Runnable[str, dict]):
    def invoke(self, text: str):
        
        return {
            "answer": text
        }