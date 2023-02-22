class CharacterModelMetaData(object):
    def __init__(self, CharacterType, GenderType, EthnicityType):
        self.CharacterType = CharacterType
        self.GenderType = GenderType
        self.EthnicityType = EthnicityType


class CharacterModelData(object):
    def __init__(self, uid, metaData):
        self.uid = uid
        self.metaData = CharacterModelMetaData(**metaData)
