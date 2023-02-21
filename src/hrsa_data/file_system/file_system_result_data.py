from dataclasses import dataclass, field


@dataclass
class FileSystemResultData:
    is_success: bool = field(default=False)
    error_message: str = field(default='')
    message: str = field(default='')
    # TODO: Add error_code data class to specify the error codes
    error_code: int = field(default=0)
