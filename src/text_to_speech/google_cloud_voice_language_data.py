from dataclasses import dataclass, field

from text_to_speech.google_cloud_voice_gender_data import GoogleCloudVoiceGenderData


@dataclass
class GoogleCloudVoiceLanguageData:
    language_code: str = field(default='')
    language_name: str = field(default='')
    gender_data: GoogleCloudVoiceGenderData = field(default_factory=GoogleCloudVoiceGenderData)
