from dataclasses import dataclass, field

from .google_cloud_translate_language_data import GoogleCloudTranslateLanguageData


@dataclass
class GoogleCloudTranslateData:
    language_data: dict[str, GoogleCloudTranslateLanguageData] = field(default_factory=dict)
