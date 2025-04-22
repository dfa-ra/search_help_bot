from dataclasses import dataclass
from typing import Optional, List

from core.models import Request


@dataclass
class CompletableRequestsResult:
    success: bool
    list: List[Request]
    message: Optional[str] = None
    error: Optional[Exception] = None

    @staticmethod
    def ok(message: str = "", list: List[Request] = None, success: bool = True):
        return CompletableRequestsResult(success=True, message=message, list=list)

    @staticmethod
    def fail(error: Exception, message: str = ""):
        return CompletableRequestsResult(success=False, error=error, message=message)

    def is_success(self):
        return self.success

    def is_failure(self):
        return not self.success
