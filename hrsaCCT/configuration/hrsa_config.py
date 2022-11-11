import json

class SubtitleConfig(object):
    def __init__(self, text_color):
        self.text_color = text_color

    def toJson(self):
        return {"text_color": self.text_color}


class UIConfig(object):
    def __init__(self, subtitle):
        self.subtitle = SubtitleConfig(**subtitle)

    def toJson(self):
        return {"subtitle": self.subtitle.toJson()}


class CharacterConfig(object):
    def __init__(self, ui):
        self.ui = UIConfig(**ui)

    def toJson(self):
        return {"ui": self.ui.toJson()}


class HRSAConfig(object):
    def __init__(self, player, medicalstudent, patient, trainer):
        self.player = CharacterConfig(**player)
        self.medicalstudent = CharacterConfig(**medicalstudent)
        self.patient = CharacterConfig(**patient)
        self.trainer = CharacterConfig(**trainer)

    def toJson(self):
        return {"player": self.player.toJson(), "medicalstudent": self.medicalstudent.toJson(), "patient": self.patient.toJson(), "trainer": self.trainer.toJson() }