from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

class PromptBuilder:

    def build_prompt(data):
        df = data["df"]
        question = data["question"]

        return """
            You are an assistant answering questions about a dataset.

            Dataset:

            {dataset_text}

            Question:
            {question}

            Answer:
            """
    PromptBuilder = RunnableLambda(build_prompt)


pipe = pipeline(
    "text-generation",
    model="HuggingFaceTB/SmolLM2-135M-Instruct",
)

LLMRunner = HuggingFacePipeline(pipeline=pipe)


ResponeParser = StrOutputParser()