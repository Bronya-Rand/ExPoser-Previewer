
init -1 python:
    available_characters = dict()

    class ExposerPreviewerInput(object):
        def __init__(self, **kwargs):
            self.pose_input = ""

            for key, value in kwargs.items():
                setattr(self, key, "")

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

    placeholder = ExposerPreviewerDefinition(
        char="Placeholder",
        pose=None
    )
