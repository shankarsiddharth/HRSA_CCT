from dataclasses import dataclass, field


@dataclass
class GoogleCloudTranslateResponseElementData:
    original_text: str = field(default='')
    translated_text: str = field(default='')
