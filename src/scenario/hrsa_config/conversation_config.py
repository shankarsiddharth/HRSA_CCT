from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConversationConfig:
    question_timer_in_seconds: int = field(default=0)

    @staticmethod
    def from_dict(obj: Any) -> 'ConversationConfig':
        _question_timer_in_seconds = int(obj.get("question_timer_in_seconds"))
        return ConversationConfig(
            _question_timer_in_seconds
        )
