import pandas as pd
from app.chain.steps import ContextBuilder, PromptBuilder, LLMRunner, ResponeParser
from app.schemas import DatasetQuestion, DatasetContext
from app.chain.pipeline import chain
from unittest.mock import patch

def test_ContextBuilder():
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Carol"],
        "grade": [85, 91, 97]
    })

    data = DatasetQuestion(
        df=df,
        question="Who has the highest grade?"
    )

    result = ContextBuilder().invoke(data)
    assert "Carol" in result.context
    assert "97" in result.context

def test_prompt_builder():
    df = pd.DataFrame({
        "Name": ["Gustav", "Kajsa"],
        "Age": [31, 35]
    })

    data = DatasetQuestion(
        df=df,
        question="Who has the highest age?"
    )

    context = ContextBuilder().invoke(data)
    prompt= PromptBuilder().invoke(context)

    assert "Kajsa" in prompt
    assert "35" in prompt
    assert "Who has the highest age?" in prompt

@patch("app.chain.steps.pipe")
def test_llm_runner(mock_pipe):
    mock_pipe.return_value = [
        {
            "generated_text": "67"
        }
    ]

    runner = LLMRunner()
    result = runner.invoke("What is the answer?")

    assert result["response"] == "67"

def test_response_parser():
    parser = ResponeParser()

    data = {
        "prompt": """
        Question:
        Who?
        Sentence:
        """,
        "response": "Thomas",
        "model": "MockLLM"
    }

    result = parser.invoke(data)

    assert result["Question"] == "Who?"
    assert result["Answer"] == "Thomas"
    assert result["Model"] == "MockLLM"

def test_chain_run():
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Carol"],
        "grade": [85, 91, 97]
    })

    data = DatasetQuestion(
        df=df,
        question="Who has the highest grade?"
    )

    result = chain.invoke(data)
    assert isinstance(result, dict)
    assert "Question" in result
    assert "Answer" in result
    assert "Model" in result
