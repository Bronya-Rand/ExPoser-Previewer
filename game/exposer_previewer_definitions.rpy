
python early:
    import string

init -1 python:
    available_characters = dict()

    class ExposerDDLCDefinition():
        def __init__(self, ddlc_poses, ddlc_expressions, ddlc_special_pose, ddlc_special_expressions):
            self.ddlc_poses = ddlc_poses
            self.ddlc_expressions = ddlc_expressions
            self.ddlc_special_pose = ddlc_special_pose
            self.ddlc_special_expressions = ddlc_special_expressions

    class ExposerPreviewerDefinition():
        def __init__(self, char, supports_exposer, poses, exposer_poses, outfits, moods, blushes, left_poses, right_poses, head, head_noses, head_mouths, head_eyes, head_eyebrows, noses, mouths, eyes, eyebrows, specials, second_poses, second_moods, second_blushes, second_noses, second_mouths, second_eyes, second_eyebrows, ddlc=False, ddlc_poses=[], ddlc_expressions=[], ddlc_special_pose=[], ddlc_special_expressions=[]):
            global available_characters

            self.char = char.lower()
            self.supports_exposer = supports_exposer
            self.poses = poses
            self.exposer_poses = exposer_poses
            self.outfits = outfits
            self.moods = moods
            self.blushes = blushes
            self.left_poses = left_poses
            self.right_poses = right_poses
            self.head = head
            self.head_noses = head_noses
            self.head_mouths = head_mouths
            self.head_eyes = head_eyes
            self.head_eyebrows = head_eyebrows
            self.noses = noses
            self.mouths = mouths
            self.eyes = eyes
            self.eyebrows = eyebrows
            self.specials = specials
            self.second_poses = second_poses
            self.second_moods = second_moods
            self.second_blushes = second_blushes
            self.second_noses = second_noses
            self.second_mouths = second_mouths
            self.second_eyes = second_eyes
            self.second_eyebrows = second_eyebrows
            self.ddlc = ddlc
            if ddlc:
                self.ddlc_def = ExposerDDLCDefinition(
                    ddlc_poses = ddlc_poses,
                    ddlc_expressions = ddlc_expressions,
                    ddlc_special_pose = ddlc_special_pose,
                    ddlc_special_expressions = ddlc_special_expressions
                )
            else:
                self.ddlc_def = None

            available_characters[self.char] = self

    placeholder = ExposerPreviewerDefinition(
        char="placeholder",
        supports_exposer=False,
        poses=[],
        exposer_poses=[],
        outfits=[],
        moods=[],
        blushes=[],
        left_poses=[],
        right_poses=[],
        head=[],
        head_noses=[],
        head_mouths=[],
        head_eyes=[],
        head_eyebrows=[],
        noses=[""], # Keep the first element as ""
        mouths=[""],
        eyes=[""],
        eyebrows=[""],
        specials=[],
        second_poses=[],
        second_moods=[],
        second_blushes=[],
        second_noses=[""], # Keep the first element as ""
        second_mouths=[""],
        second_eyes=[""],
        second_eyebrows=[""],
        ddlc = False
    )