class CharacterModelMetaData(object):
    def __init__(self, CharacterType, GenderType, EthnicityType, PreviewLabel):
        self.CharacterType = CharacterType
        self.GenderType = GenderType
        self.EthnicityType = EthnicityType
        self.PreviewLabel = PreviewLabel


class CharacterModelData(object):
    def __init__(self, uid, metaData):
        self.uid = uid
        self.metaData = CharacterModelMetaData(**metaData)
