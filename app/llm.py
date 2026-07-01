from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline


pipe = pipeline(
    "text-generation",
    model="HuggingFaceTB/SmolLM2-135M-Instruct",
    do_sample=False,
    max_new_tokens=200
)

llm = HuggingFacePipeline(pipeline=pipe)