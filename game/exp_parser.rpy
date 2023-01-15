# Parser Classes and Functions
init -3 python in exp_pasrer:  
    from renpy import store
    from renpy.character import ADVCharacter

    class ExPoserCharacter(object):
        def __init__(self, tag):
            self.tag = tag
            self.attributes_map = {}

    class ExPoserDDLCCharacter(object):
        def __init__(self, tag):
            self.tag = tag
            self.attributes_map = []

    class AttributeDict(object):
        def __init__(self):
            self.attributes = {}
        
        def append(self, key, value):
            if not self.attributes.has_key(key):
                self.attributes[key] = value
            else:
                # Ren'Py 7 hates [set()] so tell it to convert the set to list again
                self.attributes[key] = list(set(self.attributes[key] + value))

    def get_characters():
        characters = []
        for var, c in store.__dict__.items():
            char = getattr(store, var)
            if isinstance(char, ADVCharacter):
                if char.__dict__['dynamic'] and char.__dict__['image_tag']:
                    characters.append(char.__dict__['image_tag'])
        return characters

    characters = {}
    ddlc_characters = {}

# LayeredImage Parser
init -2 python hide:
    from store.exp_pasrer import ExPoserCharacter, AttributeDict

    if not renpy.get_autoreload():

        if config.developer:
            characters = exp_pasrer.get_characters()

            # For Every Character from the characters array
            for c in characters:
                # For the character name and image defined in Ren'Py
                for name, image in renpy.display.image.images.items():
                    # Set name and attribute as tag and tag_rest
                    tag, tag_rest = name[0], name[1:]
                    if tag != c: continue
                    
                    if not isinstance(image, LayeredImage): continue

                    exp_pasrer.characters.setdefault(c, ExPoserCharacter(tag))

                    last_group = None

                    # Stores the group and attributes in a dict class
                    attr_dict = AttributeDict()

                    # For every attribute
                    for attr in image.attributes:
                        # do not include the always attribute
                        if isinstance(attr, layeredimage.Always): continue

                        if last_group is None or attr.group != last_group:
                            last_group = attr.group

                        # Add "" first to remove certain areas
                        attr_dict.append(attr.group, ["", attr.attribute])

                    exp_pasrer.characters[c].attributes_map[tag_rest] = attr_dict

            # Translate all groups and attributes for every character's pose to ExPoser Previewer
            for tag, c in exp_pasrer.characters.items():
                for pose, attr_dict in c.attributes_map.items():
                    fileName = "%s_%s" % (tag, "".join(pose))

                    with open(os.path.join(config.gamedir, "exposer_defs", fileName + "_def.rpy"), "w") as edf:
                        edf.write("init python:\n")
                        edf.write(
                            "    ExposerPreviewerDefinition(\n"
                        )
                        edf.write("        char=\"%s (%s)\",\n" % (tag.capitalize(), " ".join(pose).capitalize()))
                        edf.write("        pose=\"%s %s\",\n" % (tag, " ".join(pose)))
                        for g, attributes in c.attributes_map[pose].attributes.items():
                            edf.write("        {0}={1},\n".format(g, sorted(attributes)))
                        edf.write("    )\n")

init -2 python:
    from re import compile
    from store.exp_pasrer import ExPoserDDLCCharacter, AttributeDict

    def get_ddlc_syntax():

        ddlc_casual_re = compile(r"\S+b\S+")

        if not renpy.get_autoreload():

            if config.developer:
                characters = exp_pasrer.get_characters()
                for c in characters:
                    exp_pasrer.ddlc_characters.setdefault(c, ExPoserDDLCCharacter(c))

                    for name, image in renpy.display.image.images.items():
                        # Set name and attribute as tag and tag_rest
                        tag, tag_rest = name[0], name[1:]
                        if tag != c: continue
                    
                        # Do not check for layeredimages
                        if not isinstance(image, renpy.display.im.Composite): continue

                        exp_pasrer.ddlc_characters[c].attributes_map.append(name[1])
                    
                    if exp_pasrer.ddlc_characters[c].attributes_map == []:
                        del exp_pasrer.ddlc_characters[c]

                for tag, c in exp_pasrer.ddlc_characters.items():
                    fileName = "%s_ddlc" % (tag)

                    with open(os.path.join(config.gamedir, "exposer_defs", fileName + "_def.rpy"), "w") as edf:
                        edf.write("init python:\n")
                        edf.write(
                            "    ExposerPreviewerDDLCDefinition(\n"
                        )
                        edf.write("        char=\"%s\",\n" % (tag))
                        casual = []
                        uniform = []
                        for attrs in c.attributes_map:
                            if ddlc_casual_re.match(attrs):
                                casual.append(attrs)
                            else:
                                uniform.append(attrs)
                        edf.write("        uniform={0},\n".format(sorted(uniform)))
                        edf.write("        casual={0},\n".format(sorted(casual)))
                        edf.write("    )\n")

init -1 python:
    config.start_callbacks += [get_ddlc_syntax]