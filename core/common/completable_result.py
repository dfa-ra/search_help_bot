from dataclasses import dataclass
from typing import Optional

from core.common.CustomErrors import ErrorTypes


@dataclass
class CompletableResult:
    success: bool
    message: Optional[str] = None
    error: Optional[Exception] = None
    error_type: int = None

    @staticmethod
    def ok(message: str = ""):
        return CompletableResult(success=True, message=message)

    @staticmethod
    def fail(error: Exception, message: str = "", error_type: int = None):
        return CompletableResult(success=False, error=error, message=message, error_type=error_type)

    def is_success(self):
        return self.success

    def is_failure(self):
        return not self.success
