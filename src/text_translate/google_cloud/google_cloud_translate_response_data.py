from dataclasses import dataclass, field

from .google_cloud_translate_response_element_data import GoogleCloudTranslateResponseElementData


@dataclass
class GoogleCloudTranslateResponseData:
    response_data: dict[int, GoogleCloudTranslateResponseElementData] = field(default_factory=dict)
