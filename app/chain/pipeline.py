from .steps import PromptBuilder
from .steps import LLMRunner
from .steps import ResponeParser

chain = ( PromptBuilder | LLMRunner | ResponeParser )