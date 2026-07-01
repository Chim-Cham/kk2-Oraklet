from langchain_core.output_parsers import StrOutputParser
from .llm import llm
from .prompts_template import summarize_prompt

chain = summarize_prompt | llm | StrOutputParser()