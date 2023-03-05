from dataclasses import dataclass, field


@dataclass
class GoogleCloudVoiceGenderData:
    MALE: list[str] = field(default_factory=list)
    FEMALE: list[str] = field(default_factory=list)
    NEUTRAL: list[str] = field(default_factory=list)
