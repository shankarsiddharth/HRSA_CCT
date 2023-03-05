from dataclasses import dataclass, field


@dataclass
class GoogleCloudTranslateLanguageData:
    language_code: str = field(default='')
    language_name: str = field(default='')
