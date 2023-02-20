from dataclasses import dataclass, field
from typing import Any


@dataclass
class CharacterVoiceConfig:
    language_code: str = field(default='')
    gender: str = field(default='')
    voice_name: str = field(default='')
    language: str = field(default='')
    model: str = field(default='')

    @staticmethod
    def from_dict(obj: Any) -> 'CharacterVoiceConfig':
        _language_code = str(obj.get("language_code"))
        _gender = str(obj.get("gender"))
        _voice_name = str(obj.get("voice_name"))
        _language = str(obj.get("language"))
        _model = str(obj.get("model"))
        return CharacterVoiceConfig(
            _language_code,
            _gender,
            _voice_name,
            _language,
            _model
        )
