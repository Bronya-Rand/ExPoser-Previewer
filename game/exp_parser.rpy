
# LayeredImage Parser
init 1 python in exp_previewer:
    from collections import OrderedDict
    from store import LayeredImage

    # Grab all LayeredImage Char Names
    layeredimages = OrderedDict(sorted({name[0]: {} for name, image in renpy.display.image.images.items()
        if isinstance(image, LayeredImage)}.items()))

    def fetch_layeredim6age_obj():
        """
        This function obtains the layeredimage classes for each character.
        """
        layeredimages["placeholder"] = (None, None)
        for name, image in renpy.display.image.images.items():
            if isinstance(image, LayeredImage):
                layeredimages[name[0]][name[1]] = image
                
    fetch_layeredimage_obj()