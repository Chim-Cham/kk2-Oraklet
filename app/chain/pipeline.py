from .steps import ContextBuilder, PromptBuilder, LLMRunner, ResponeParser


chain = ( ContextBuilder() | PromptBuilder() | LLMRunner() | ResponeParser() )