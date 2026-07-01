from pydantic import BaseModel, ConfigDict, SerializeAsAny
from typing import Any, Callable, Generic, TypeVar

I = TypeVar("I")
O = TypeVar("O")
M = TypeVar("M")

class Runnable(BaseModel, Generic[I, O]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str | None = None

    def invoke(self, data: I) -> O:
        raise NotImplementedError()
    
    def __or__(self, other: Any):
        if isinstance(other, Runnable):
            return RunnableSequence(
                first=self,
                second=other
            )
        
        if callable(other):
            return RunnableSequence(
                first=self,
                second=RunnableLabda(func=other)
            )
        
        return NotImplemented
    

class RunnableLabda(Runnable[I, O]):
    func: Callable[[I], O]

    def invoke(self, data: I) -> O:
        return self.func(data)


class RunnableSequence(Runnable[I, O]):
    first: SerializeAsAny[Runnable[I, M]]
    second: SerializeAsAny[Runnable[M, O]]

    def invoke(self, data: I) -> O:
        intermediate = self.first.invoke(data)
        return self.second.invoke(intermediate)