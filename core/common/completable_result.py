from dataclasses import dataclass
from typing import Optional


@dataclass
class CompletableResult:
    success: bool
    message: Optional[str] = None
    error: Optional[Exception] = None

    @staticmethod
    def ok(message: str = ""):
        return CompletableResult(success=True, message=message)

    @staticmethod
    def fail(error: Exception, message: str = "" ):
        return CompletableResult(success=False, error=error, message=message)

    def is_success(self):
        return self.success

    def is_failure(self):
        return not self.success
