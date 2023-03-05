from dataclasses import dataclass, field

from .google_cloud_voice_language_data import GoogleCloudVoiceLanguageData


@dataclass
class GoogleCloudVoiceData:
    voice_data: dict[str, GoogleCloudVoiceLanguageData] = field(default_factory=dict)
    '''
    {
        "en_US": {
            "language_code": "en_US",
            "language_name": "English (United States)",
            "gender_data": {
                "gender1": [
                    "voice_name_list"
                ],
                "gender2": [
                    "voice_name_list"
                ]
            }
        },
        "zh_CN": {
            "language_code": "zh_CN",
            "language_name": "Chinese (China)",
            "gender_data": {
                "gender1": [
                    "voice_name_list"
                ],
                "gender2": [
                    "voice_name_list"
                ]
            }
        }
    }
    '''
    pass
