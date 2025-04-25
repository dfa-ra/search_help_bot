from dataclasses import dataclass
from typing import Optional

from core.models import FileModel


@dataclass
class CompletableFileResult:
    success: bool
    message: Optional[str] = None
    error: Optional[Exception] = None
    file: Optional[FileModel] = None

    @staticmethod
    def ok(message: str = "", file: Optional[FileModel] = None):
        return CompletableFileResult(success=True, message=message, file=file)

    @staticmethod
    def fail(error: Exception, message: str = "", error_type: int = None):
        return CompletableFileResult(success=False, error=error, message=message)

    def is_success(self):
        return self.success

    def is_failure(self):
        return not self.success