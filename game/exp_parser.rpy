
# LayeredImage Parser
init 1 python in exp_previewer:
    from renpy import store
    from collections import OrderedDict
    from store import LayeredImage, ADVCharacter

    # Grab all LayeredImage Char Names
    layeredimages = OrderedDict(sorted({name[0]: {} for name, image in renpy.display.image.images.items()
        if isinstance(image, LayeredImage)}.items()))
    ddlcimages = None
    backgrounds = {}

    def fetch_layeredimage_obj():
        """
        This function obtains the layeredimage classes for each character.
        """
        layeredimages["placeholder"] = (None, None)
        for name, image in renpy.display.image.images.items():
            if isinstance(image, LayeredImage):
                layeredimages[name[0]][name[1]] = image

    def fetch_ddlcimage_pattern():
        """
        This function obtains the image pattern for each character that is a ADVCharacter.
        """
        # Due to the nature that some chars image might not be Composite's
        # grab names of actual characters
        characters = []
        for var, c in store.__dict__.items():
            char = getattr(store, var)
            if isinstance(char, ADVCharacter):
                # Let's only focus on the image tag for now than dynamic.
                if char.__dict__['image_tag']:
                    characters.append(char.__dict__['image_tag'])

        temp = OrderedDict(sorted({c: [] for c in characters}.items()))
        temp["placeholder"] = []

        for c in characters:
            for name, image in renpy.display.image.images.items():
                if name[0] != c: continue
                if name[0] in layeredimages.keys():
                    if name[1] in layeredimages[c].keys(): continue 
                temp[name[0]].append(name[1])

        return temp
    
    def fetch_backgrounds():
        """
        This function obtains all images with a bg tag on them.
        """
        for name, image in renpy.display.image.images.items():
            if name[0] == "bg":
                if isinstance(image, renpy.display.im.Image):
                    backgrounds[name[0] + " " + name[1]] = image

    def run_postboot_fetcher():
        ddlcimages = fetch_ddlcimage_pattern()
        fetch_backgrounds()

    fetch_layeredimage_obj()