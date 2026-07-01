from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline


pipe = pipeline(
    "text-generation",
    model="HuggingFaceTB/SmolLM2-135M-Instruct",
    max_new_tokens=150,
    return_full_text=False,
    do_sample=False
)


llm = HuggingFacePipeline(pipeline=pipe)