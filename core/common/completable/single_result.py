from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar('T')


@dataclass
class SingleResult(Generic[T]):
    """класс обёртка для возврата какого-либо значения из  сервисов"""
    success: bool
    result: Optional[T] = None
    result_type: Optional[type] = None
    message: Optional[str] = None
    my_error: Optional[Exception] = None
    error_type: Optional[int] = None

    @classmethod
    def ok(cls, result: Optional[T] = None, message: str = "") -> 'SingleResult[T]':
        return cls(success=True, result=result, message=message, result_type=type(result))

    @classmethod
    def fail(my_error: Exception, message: str = "", error_type: int = None):
        return SingleResult(success=False, my_error=my_error, message=message, error_type=error_type)

    def is_success(self):
        return self.success

    def is_failure(self):
        return not self.success
