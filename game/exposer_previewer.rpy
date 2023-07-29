
define total_characters = 1 
default persistent.exp_first_run = False
define hide_preview_code = False
define exp_ver = "2.12"
define exp_background = "bg club_day"

init -1000 python:
    def _exp_overlay():
        renpy.show_screen("new_exposer_previewer")
        renpy.restart_interaction()

    config.keymap['exp_overlay'] = ['shift_K_F5']
    config.underlay.append(
        renpy.Keymap(
        exp_overlay = _exp_overlay
        )
    )

init python:
    import pygame_sdl2.scrap
    import string
    from store import exp_previewer

    class ExPoserCharacter():
        placeholder = Placeholder("girl", text="Placeholder")

        def __init__(self):
            self.char = "placeholder"
            self.pose = ""
            self.zoom_size = 0.76
            self.attrs = {}
            # For now the only efficient way to hide vboxes from viewport
            self.attrs_vars = {}
            self.ddlc_attr = ""
            self.ddlc_mode = False

        def initialize_attributes(self, pose=None, reset=False):
            if self.char != "placeholder":
                if not self.ddlc_mode:
                    if pose is None:
                        pose = next(iter(exp_previewer.layeredimages[self.char].keys()))
                    if reset:
                        self.attrs = dict.fromkeys(exp_previewer.layeredimages[self.char][pose].group_to_attributes.keys(), "")
                    self.attrs_vars = dict.fromkeys(exp_previewer.layeredimages[self.char][pose].group_to_attributes.keys(), False)
                    self.attrs_vars['poses'] = False
                else: 
                    if reset:
                        if pose is None:
                            pose = next(iter(exp_previewer.ddlcimages[self.char]))
                        self.ddlc_attr = pose

        def set_attr(self, group, new_attr):
            if self.char != "placeholder":
                self.attrs[group] = new_attr
        
        def set_ddlc_attr(self, new_attr):
            self.ddlc_attr = new_attr

        def get_attr_input(self):
            if self.char != "placeholder":
                if not self.ddlc_mode:
                    return " ".join(str(attr) for attr in self.attrs.values() if attr != "")
                return self.ddlc_attr
            return ""

        def set_char_data(self, new_character, p=None):
            self.char = new_character
            if new_character != "placeholder":
                if not self.ddlc_mode:
                    if not p:
                        p = next(iter(exp_previewer.layeredimages[self.char].keys()))
                    self.pose = p
                else:
                    p = next(iter(exp_previewer.ddlcimages[self.char]))
                self.initialize_attributes(p, reset=True)
                return

        def parse_input_data(self):
            if self.char != "placeholder":
                if not self.ddlc_mode:
                    d = self.char + " " + self.pose + " " + self.get_attr_input()
                else:
                    d = self.char + " " + self.get_attr_input()
                if new_can_show(d):
                    return d, self.zoom_size
            return self.placeholder, 1.0
        
        def reset(self):
            self.char = "placeholder"
            self.zoom_size = 0.76

    char1 = ExPoserCharacter()
    char2 = ExPoserCharacter()
    char3 = ExPoserCharacter()
    char4 = ExPoserCharacter()

    selected_character = char1
    left_side_chars = [char1, char2]

    def calculate_dsr():
        return config.screen_width / 1280.0

    dsr_scale = calculate_dsr()

    def copy_line(c):
        if c.char != "placeholder":
            if not c.ddlc_mode:
                l = "show " + c.char + " " + c.pose + " " + c.get_attr_input()
            else:
                l = "show " + c.char + " " + c.get_attr_input()
            pygame_sdl2.scrap.put(pygame_sdl2.scrap.SCRAP_TEXT, l.encode("utf-8"))
            renpy.show_screen("dialog", message="Copied syntax of this character to the clipboard.", ok_action=Hide("dialog"))
        else:
            renpy.show_screen("dialog", message="Cannot copy syntax of a placeholder character.", ok_action=Hide("dialog"))
    
    def char_switch(char_obj, back=False):
        current_character = char_obj.char
        if char_obj.ddlc_mode:
            character_names = list(exp_previewer.ddlcimages.keys())
        else:
            character_names = list(exp_previewer.layeredimages.keys())
        current_index = character_names.index(current_character)

        # Get the next character name index based on the back flag
        next_index = current_index - 1 if back else current_index + 1

        # Wrap around the index if it goes beyond the list bounds
        next_index %= len(character_names)

        # Get the next character name from the list
        next_character = character_names[next_index]

        # Set the new character name and update DictNavigator
        char_obj.set_char_data(next_character)

    def calculate_xpos(i):
        if total_characters == 2:
            return int(400 * dsr_scale) + ((i-1) * int(480*dsr_scale))
        if total_characters == 3:
            return int(240 * dsr_scale) + ((i-1) * int(400*dsr_scale))
        if total_characters == 4:
            return int(200 * dsr_scale) + ((i-1) * int(293*dsr_scale))
        return int(640 * dsr_scale)
    
    # 7.5.X/8.0.X can_show cuz <7.4.11 causes issues
    def new_can_show(name, layer=None, tag=None):
        if not isinstance(name, tuple):
            name = tuple(name.split())
        if tag is None:
            tag = name[0]

        layer = renpy.default_layer(layer, tag)
        try:
            return renpy.game.context().images.apply_attributes(layer, tag, name)
        except:
            return None

    def img_can_show(img):
        if img == "": return False
        if new_can_show(exp_background) is None:
            try:
                renpy.loader.load(exp_background)
                return True
            except IOError:
                return False
        return True

screen new_exposer_previewer:
    tag menu
    
    style_prefix "exposer_previewer"

    python:
        can_load = img_can_show(exp_background)
    
    if can_load:
        add exp_background
    else:
        add Solid("#000")
        text "Unable to load image path: " + exp_background color "#ff0000" size int(16 * dsr_scale)

    python:
        char1_sprite_show, char1_sprite_zoom = char1.parse_input_data()
        char2_sprite_show, char2_sprite_zoom = char2.parse_input_data()
        char3_sprite_show, char3_sprite_zoom = char3.parse_input_data()
        char4_sprite_show, char4_sprite_zoom = char4.parse_input_data()
        
    fixed:
        add Transform(char1_sprite_show, zoom=char1_sprite_zoom, xcenter=calculate_xpos(1))
        if total_characters >= 2:
            add Transform(char2_sprite_show, zoom=char2_sprite_zoom, xcenter=calculate_xpos(2))
        if total_characters >= 3:
            add Transform(char3_sprite_show, zoom=char3_sprite_zoom, xcenter=calculate_xpos(3))
        if total_characters == 4:
            add Transform(char4_sprite_show, zoom=char4_sprite_zoom, xcenter=calculate_xpos(4))

    if not hide_preview_code:
        vbox:
            if total_characters == 1 or (total_characters == 2 and selected_character in left_side_chars[:1]) or (total_characters >= 3 and selected_character in left_side_chars):
                xalign 0.05
            else:
                xalign 0.95
            yalign 0.95

            if selected_character.char != "placeholder":
                vbox:
                    text "Zoom Size (" + str(round(selected_character.zoom_size, 2)) + "): "
                    hbox:
                        xoffset 10
                        bar value FieldValue(selected_character, "zoom_size", 1.0) xmaximum 110
                        textbutton "R" action SetField(selected_character, "zoom_size", 0.76)
                textbutton "Copy Pose Data" action Function(copy_line, selected_character)
            textbutton "Change Scene" action Show("exposer_scene_grid")
            textbutton "Reset Char" action Function(selected_character.reset)
            textbutton "Pose Menu" action If(renpy.get_screen("exposer_pose_menu"), Hide("exposer_pose_menu"), Show("exposer_pose_menu"))
            hbox:
                textbutton "Exit" action [Hide("exposer_pose_menu"), Return()]
                textbutton "(i)" action Show("dialog", message="ExPoser Previewer [exp_ver]\nCopyright © 2022-2023 GanstaKingofSA. All rights reserved.", ok_action=Hide("dialog")) text_size int(16 * dsr_scale)

    on "show" action [Function(exp_previewer.fetch_ddlcimage_pattern), Function(exp_previewer.fetch_backgrounds)] # Fixes Autoreload for DDLC syntax.
    on "replace" action [Function(exp_previewer.fetch_ddlcimage_pattern), Function(exp_previewer.fetch_backgrounds), If(persistent.exp_first_run, None, Show("dialog", message="Welcome to {u}ExPoser Previewer!{/u}\nThis tool allows you to pose characters in real-time using the 'Pose Menu' from\nDDLC's own poses, to Mood Pose Tool poses and even ExPoser poses.\n\nBe advised that this tool might have bugs. If a bug is found, please\nreport them.", ok_action=[SetField(persistent, "exp_first_run", True), Hide("dialog")]))]
    key "mouseup_3" action ToggleVariable("hide_preview_code")

screen exposer_pose_menu:
    style_prefix "exposer_previewer"

    if not hide_preview_code:
        if total_characters == 1 or (total_characters == 2 and selected_character in left_side_chars[:1]) or (total_characters >= 3 and selected_character in left_side_chars):
            add Transform(Solid("#000"), alpha=0.75) xpos int(820 * dsr_scale) xsize int(460 * dsr_scale)
        else: 
            add Transform(Solid("#000"), alpha=0.75) xsize int(460 * dsr_scale)

        fixed:
            if total_characters == 1 or (total_characters == 2 and selected_character in left_side_chars[:1]) or (total_characters >= 3 and selected_character in left_side_chars):
                xpos int(820 * dsr_scale)
            vbox:
                xoffset 25
                spacing 5
                null height 10

                hbox:
                    xoffset -10
                    text "Character "
                    textbutton "<" action Function(char_switch, selected_character, True)
                    null width 5
                    vbox:
                        xsize int(260 * dsr_scale)
                        text selected_character.char.capitalize() xalign 0.5
                    null width 5
                    textbutton ">" action Function(char_switch, selected_character)

                hbox:
                    xoffset -10
                    spacing 2
                    text "# of Chars "
                    textbutton "1" action [SetVariable("total_characters", 1), SensitiveIf(total_characters != 1)]
                    textbutton "2" action [SetVariable("total_characters", 2), SensitiveIf(total_characters != 2)]
                    textbutton "3" action [SetVariable("total_characters", 3), SensitiveIf(total_characters != 3)]
                    textbutton "4" action [SetVariable("total_characters", 4), SensitiveIf(total_characters != 4)]

                    null width 10

                    hbox:
                        spacing 3
                        text "Char "
                        textbutton "1" action [Function(char1.initialize_attributes), SetVariable("selected_character", char1), SensitiveIf(selected_character != char1)]
                        if total_characters >= 2:
                            textbutton "2" action [Function(char2.initialize_attributes), SetVariable("selected_character", char2), SensitiveIf(selected_character != char2)]
                        if total_characters >= 3:
                            textbutton "3" action [Function(char3.initialize_attributes), SetVariable("selected_character", char3), SensitiveIf(selected_character != char3)]
                        if total_characters == 4:
                            textbutton "4" action [Function(char4.initialize_attributes), SetVariable("selected_character", char4), SensitiveIf(selected_character != char4)]

                if selected_character.char != "placeholder":
                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        xmaximum int(420 * dsr_scale)
                        ymaximum int(620 * dsr_scale)
                        has vbox

                        hbox:
                            xalign .5
                            python:
                                img_syntax = "LayeredImage (MPT/ExPoser)"
                                if selected_character.ddlc_mode:
                                    img_syntax = "DDLC"
                            text "Syntax: " + img_syntax size int(16 * dsr_scale)
                            textbutton "Change Syntax":
                                text_size int(14 * dsr_scale)
                                yoffset -4
                                action [ToggleField(selected_character, "ddlc_mode", False, True), Function(selected_character.reset)]

                        if not selected_character.ddlc_mode:
                            python:
                                carrot_arrow = ">" if not selected_character.attrs_vars['poses'] else "v"

                            textbutton carrot_arrow + " Poses":
                                text_size int(16 * dsr_scale)
                                action ToggleDict(selected_character.attrs_vars, "poses", False, True)

                            if selected_character.attrs_vars['poses']:
                                vbox:   
                                    xoffset 20
                                    for p in exp_previewer.layeredimages[selected_character.char].keys():
                                        python:
                                            if p == "":
                                                pose_text = "Unknown Pose Name"
                                            else:
                                                pose_text = p
                                        textbutton pose_text:
                                            text_size int(16 * dsr_scale)
                                            action [Function(selected_character.set_char_data, selected_character.char, p), SensitiveIf(p != selected_character.pose)]
                                
                            for g, attr in exp_previewer.layeredimages[selected_character.char][selected_character.pose].group_to_attributes.items():
                                python:
                                    carrot_arrow = ">" if not selected_character.attrs_vars[g] else "v"

                                textbutton carrot_arrow + " " + g:
                                    text_size int(16 * dsr_scale)
                                    action ToggleDict(selected_character.attrs_vars, g, False, True)

                                if selected_character.attrs_vars[g]:
                                    vbox:   
                                        xoffset 20
                                        textbutton "None":
                                            text_size int(16 * dsr_scale)
                                            action [Function(selected_character.set_attr, g, ""), SensitiveIf("" != selected_character.attrs[g])]

                                        for a in sorted(attr):
                                            textbutton a:
                                                text_size int(16 * dsr_scale)
                                                action [Function(selected_character.set_attr, g, a), SensitiveIf(a != selected_character.attrs[g])]

                        else:

                            for i in exp_previewer.ddlcimages[selected_character.char]:

                                textbutton i:
                                    text_size int(16 * dsr_scale)
                                    action [Function(selected_character.set_ddlc_attr, i), SensitiveIf(i != selected_character.ddlc_attr)]

style exposer_previewer_button_text is navigation_button_text
style exposer_previewer_button:
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
style exposer_previewer_text:
    size int(18*dsr_scale)
    text_align 0.5

screen exposer_scene_grid():

    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:
        #xsize int(600 * dsr_scale)

        vbox:
            xalign .5
            label _("Select a Background"):
                style "confirm_prompt"
                xalign 0.5

            null height 20

            vpgrid:
                xalign .5
                cols 3
                ysize 450
                mousewheel True
                draggable True
                scrollbars "vertical"
                spacing 10

                python:
                    bg_count = len(exp_previewer.backgrounds)
                    if bg_count < 3:
                        null_count = 3-bg_count
                    else:
                        null_count = bg_count % 3
                
                for name, img in exp_previewer.backgrounds.items():  
                    vbox:
                        imagebutton:
                            idle Transform(img.__dict__['filename'], size=(240, 120), alpha=1.0)
                            hover Transform(img.__dict__['filename'], size=(240, 120), alpha=0.75)
                            action [Hide(), SetVariable("exp_background", name)]
                        null height 3
                        text name xalign .5 color "#000" outlines []
                
                for i in range((3-null_count)):
                    null
            
            null height 20
                
            hbox:
                xalign .5
                spacing 10
                textbutton _("Exit") action Hide()
                textbutton _("Enter Scene Name/File Path") action [Hide(), Show("exposer_scene_prompt")]

screen exposer_scene_prompt():
    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 201

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            
            label _("Input Scene Name/File Path"):
                style "confirm_prompt"
                xalign 0.5
                    
            input default "" value VariableInputValue("exp_background") color "#000" outlines []
            
            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action Hide()