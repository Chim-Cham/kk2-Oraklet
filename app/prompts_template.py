from langchain_core.prompts import ChatPromptTemplate

summarize_prompt = ChatPromptTemplate.from_template(
    """
You are an experienced data analyst.

Dataset:

{stats}

Write exactly 3 bullet points.

Do not repeat the statistics.
"""
)