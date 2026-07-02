import pandas as pd
from app.chain.steps import PromptBuilder, LLMRunner, ResponeParser
from app.schemas import DatasetQuestion
from app.chain.pipeline import chain
from unittest.mock import patch

def test_prompt_builder():
    df = pd.DataFrame({
        "name": ["Gustav", "Kajsa"],
        "age": [31, 35]
    })

    data = DatasetQuestion(
        df=df,
        question="Who is oldest?"
    )

    prompt= PromptBuilder().invoke(data)

    assert "Who is oldest" in prompt
    assert "Gustav" in prompt
    assert "Kajsa" in prompt
    assert "Dataset" in prompt

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
        Answer:
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

def test_unBias():
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Carol"],
        "grade": [85, 91, 97]
    })

    data = DatasetQuestion(
        df=df,
        question="Who has the highest grade?"
    )

    result = chain.invoke(data)
    print(result["Answer"])
    assert "Carol" in result["Answer"]
    