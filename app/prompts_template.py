from langchain_core.prompts import ChatPromptTemplate

summarize_prompt = ChatPromptTemplate.from_template(
    """
You are a data analyst.

Dataset statistics:

{stats}

Provide a concise summary.
"""
)