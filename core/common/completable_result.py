from dataclasses import dataclass
from typing import Optional


@dataclass
class CompletableResult:
    success: bool
    error: Optional[Exception] = None

    @staticmethod
    def ok():
        return CompletableResult(success=True)

    @staticmethod
    def fail(error: Exception):
        return CompletableResult(success=False, error=error)

    def is_success(self):
        return self.success

    def is_failure(self):
        return not self.success
