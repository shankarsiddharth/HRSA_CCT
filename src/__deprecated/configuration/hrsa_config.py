class DataFileVersion(object):
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def toJson(self):
        return {"major": self.major, "minor": self.minor, "patch": self.patch}


class SubtitleConfig(object):
    def __init__(self, text_color):
        self.text_color = text_color

    def toJson(self):
        return {"text_color": self.text_color}


class UIConfig(object):
    def __init__(self, subtitle_config):
        self.subtitle_config = SubtitleConfig(**subtitle_config)

    def toJson(self):
        return {"subtitle_config": self.subtitle_config.toJson()}


class ModelConfig(object):
    def __init__(self, uid):
        self.uid = uid

    def toJson(self):
        return {"uid": self.uid}


class CharacterConfig(object):
    def __init__(self, ui_config, character_model_config):
        self.ui_config = UIConfig(**ui_config)
        self.character_model_config = ModelConfig(**character_model_config)

    def toJson(self):
        return {"ui_config": self.ui_config.toJson(), "character_model_config": self.character_model_config.toJson()}


class ConversationConfig(object):
    def __init__(self, question_timer_in_seconds):
        self.question_timer_in_seconds: int = question_timer_in_seconds

    def toJson(self):
        return {"question_timer_in_seconds": int(self.question_timer_in_seconds)}


class HRSAConfig(object):
    def __init__(self, version, player_config, medicalstudent_config, patient_config, trainer_config, conversation_config):
        self.version = DataFileVersion(**version)
        self.player_config = CharacterConfig(**player_config)
        self.medicalstudent_config = CharacterConfig(**medicalstudent_config)
        self.patient_config = CharacterConfig(**patient_config)
        self.trainer_config = CharacterConfig(**trainer_config)
        self.conversation_config = ConversationConfig(**conversation_config)

    def toJson(self):
        return {
            "version": self.version.toJson(),
            "player_config": self.player_config.toJson(),
            "medicalstudent_config": self.medicalstudent_config.toJson(),
            "patient_config": self.patient_config.toJson(),
            "trainer_config": self.trainer_config.toJson(),
            "conversation_config": self.conversation_config.toJson()
        }
