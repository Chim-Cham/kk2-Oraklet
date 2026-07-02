from .steps import PromptBuilder, LLMRunner, ResponeParser


chain = ( PromptBuilder() | LLMRunner() | ResponeParser() )