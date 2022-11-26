
init -1 python:
    available_characters = {}
    available_ddlc_characters = {}

    class ExposerPreviewerInput(object):
        def __init__(self, mpt=True, **kwargs):
            self.pose_input = ""
            self.mpt = mpt

            for key, value in kwargs.items():
                self.set_key(key, "")

        def set_key(self, key, value):
            if self.mpt:
                if key == "outfit":
                    setattr(self, key, "uniform")
                elif key == "mood":
                    setattr(self, key, "neut")
                else:
                    setattr(self, key, value)
            else:
                if key == "outfit":
                    setattr(self, key, "1a")
                else:
                    setattr(self, key, value)

        def reset(self):
            for key, value in self.__dict__.items():
                if key == "mpt": continue

                self.set_key(key, "")

    class ExposerPreviewerDefinition(object):
        def __init__(self, char, pose, **kwargs):
            global available_characters

            self.char = char
            self.pose = pose
            self.input = ExposerPreviewerInput(**kwargs)
            #self.__dict__.update(kwargs)

            for key, value in kwargs.items():
                setattr(self, key, value)

            available_characters[self.char] = self

    class ExposerPreviewerDDLCDefinition(object):
        def __init__(self, char, uniform, casual):
            global available_characters

            self.char = char
            self.uniform = uniform
            self.casual = casual
            self.input = ExposerPreviewerInput(mpt=False, outfit="1a")

            available_ddlc_characters[self.char] = self

    placeholder = ExposerPreviewerDefinition(
        char="Placeholder",
        pose=None
    )

    placeholder_ddlc = ExposerPreviewerDDLCDefinition(
        char="Placeholder",
        uniform=[],
        casual=[]
    )
