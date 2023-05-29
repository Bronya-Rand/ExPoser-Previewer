
define total_characters = 1 
default persistent.exp_first_run = False
define hide_preview_code = False
define exp_ver = "2.0B"
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

    # For now the only efficient way to hide vboxes from viewport
    attrs_vars = {}

    class ExPoserCharacter():
        placeholder = Placeholder("girl", text="Placeholder")

        def __init__(self):
            self.char = "placeholder"
            self.pose = ""
            self.zoom_size = 0.76
            self.attrs = {}

        def initialize_attributes(self, pose):
            if self.char != "placeholder":
                self.attrs = dict.fromkeys(exp_previewer.layeredimages[self.char][pose].group_to_attributes.keys(), "")
                self.initialize_attr_vars(pose)

        def initialize_attr_vars(self, pose=None):
            global attrs_vars
            if self.char != "placeholder":
                if not pose: pose = self.pose
                attrs_vars = dict.fromkeys(exp_previewer.layeredimages[self.char][pose].group_to_attributes.keys(), False)
                attrs_vars['poses'] = False

        def set_attr(self, group, new_attr):
            if self.char != "placeholder":
                self.attrs[group] = new_attr

        def get_attr(self, group):
            return self.attrs.get(group, "")

        def get_attr_input(self):
            if self.char != "placeholder":
                return " ".join(str(attr) for attr in self.attrs.values() if attr != "")
            return ""

        @property
        def char(self):
            return self._char

        @char.setter
        def char(self, new_character):
            self._char = new_character
            if new_character == "placeholder":
                self.pose = ""
                self.attrs = {}
            else:
                self.pose = list(exp_previewer.layeredimages[self.char].keys())[0]
                self.initialize_attributes(self.pose)

        @property
        def pose(self):
            return self._pose

        @pose.setter
        def pose(self, new_pose):
            self._pose = new_pose
            if self.char != "placeholder":
                self.initialize_attributes(new_pose)

        def set_char_data(self, new_character, p=None):
            self.char = new_character
            if new_character != "placeholder":
                if not p:
                    p = next(iter(exp_previewer.layeredimages[self.char].keys()))
                self.pose = p
                self.initialize_attributes(p)
                return
            self.attrs = {} if new_character == "placeholder" else {group: "" for group in exp_previewer.layeredimages[self.char][p].group_to_attributes.keys()}

        def parse_input_data(self):
            if self.char != "placeholder":
                if PY2:
                    d = self.char + " " + self.pose + " " + self.get_attr_input()
                else:
                    d = f"{self.char} {self.pose} {self.get_attr_input()}"
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

    def copy_line(c):
        if c.char != "placeholder":
            l = "show " + c.char + " " + c.get_attr_input()
            pygame_sdl2.scrap.put(pygame_sdl2.scrap.SCRAP_TEXT, l.encode("utf-8"))
            renpy.show_screen("dialog", message="Copied syntax of this character to the clipboard.", ok_action=Hide("dialog"))
        else:
            renpy.show_screen("dialog", message="Cannot copy syntax of a placeholder character.", ok_action=Hide("dialog"))
    
    def char_switch(char_obj, back=False):
        current_character = char_obj.char
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

screen new_exposer_previewer:
    tag menu
    
    style_prefix "exposer_previewer"

    add exp_background
        
    fixed:
        hbox:
            python:
                default_xc = 640
                multiplier = 0
                if total_characters == 2:
                    default_xc = 400
                    multiplier = 480
                elif total_characters == 3:
                    default_xc = 240
                    multiplier = 400
                elif total_characters == 4:
                    default_xc = 200
                    multiplier = 293

            python:
                char1_sprite_show, char1_sprite_zoom = char1.parse_input_data()
                char2_sprite_show, char2_sprite_zoom = char2.parse_input_data()
                char3_sprite_show, char3_sprite_zoom = char3.parse_input_data()
                char4_sprite_show, char4_sprite_zoom = char4.parse_input_data()

            fixed:
                add Transform(char1_sprite_show, zoom=char1_sprite_zoom, xcenter=default_xc)
                if total_characters >= 2:
                    add Transform(char2_sprite_show, zoom=char2_sprite_zoom, xcenter=default_xc+multiplier)
                if total_characters >= 3:
                    add Transform(char3_sprite_show, zoom=char3_sprite_zoom, xcenter=default_xc+(multiplier*2))
                if total_characters == 4:
                    add Transform(char4_sprite_show, zoom=char4_sprite_zoom, xcenter=default_xc+(multiplier*3))

        if not hide_preview_code:
            vbox:
                if total_characters == 1 or (total_characters == 2 and selected_character == char1) or (total_characters >= 3 and (selected_character == char1 or selected_character == char2)):
                    xalign 0.05
                else:
                    xalign 0.95
                yalign 0.95

                textbutton "Change Scene" action Show("exposer_scene_prompt")
                if selected_character.char != "placeholder":
                    textbutton "Copy Pose Data" action Function(copy_line, selected_character)
                textbutton "Reset Char" action Function(selected_character.reset)
                textbutton "Pose Menu" action If(renpy.get_screen("exposer_pose_menu"), Hide("exposer_pose_menu"), Show("exposer_pose_menu"))
                hbox:
                    textbutton "Exit" action [Return()]
                    textbutton "(i)" action Show("dialog", message="ExPoser Previewer [exp_ver]\nCopyright © 2022 GanstaKingofSA. All rights reserved.", ok_action=Hide("dialog")) text_size 16

    on "replace" action If(persistent.exp_first_run, None, Show("dialog", message="Welcome to {u}ExPoser Previewer!{/u}\nThis tool allows you to pose characters in real-time using the 'Pose Menu' from\nDDLC's own poses, to Mood Pose Tool poses and even ExPoser poses.\n\nBe advised that this tool might have bugs. If a bug is found, please\nreport them.", ok_action=[SetField(persistent, "exp_first_run", True), Hide("dialog")]))
    key "mouseup_3" action ToggleVariable("hide_preview_code")

screen exposer_pose_menu:
    style_prefix "exposer_previewer"

    if not hide_preview_code:
        if total_characters == 1 or (total_characters == 2 and selected_character == char1) or (total_characters >= 3 and (selected_character == char1 or selected_character == char2)):
            add Transform(Solid("#000"), alpha=0.75) xpos 820 xsize 460
        else: 
            add Transform(Solid("#000"), alpha=0.75) xsize 460

        fixed:
            if total_characters == 1 or (total_characters == 2 and selected_character == char1) or (total_characters >= 3 and (selected_character == char1 or selected_character == char2)):
                xpos 820
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
                        xsize 260
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
                        textbutton "1" action [Function(char1.initialize_attr_vars), SetVariable("selected_character", char1), SensitiveIf(selected_character != char1)]
                        if total_characters >= 2:
                            textbutton "2" action [Function(char2.initialize_attr_vars), SetVariable("selected_character", char2), SensitiveIf(selected_character != char2)]
                        if total_characters >= 3:
                            textbutton "3" action [Function(char3.initialize_attr_vars), SetVariable("selected_character", char3), SensitiveIf(selected_character != char3)]
                        if total_characters == 4:
                            textbutton "4" action [Function(char4.initialize_attr_vars), SetVariable("selected_character", char4), SensitiveIf(selected_character != char4)]

                if selected_character.char != "placeholder":
                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        xmaximum 420
                        ymaximum 620
                        has vbox

                        python:
                            carrot_arrow = ">" if not attrs_vars['poses'] else "v"

                        textbutton carrot_arrow + " Poses":
                            text_size 16
                            action ToggleDict(attrs_vars, "poses", False, True)

                        if attrs_vars['poses']:
                            vbox:   
                                xoffset 20
                                for p in exp_previewer.layeredimages[selected_character.char].keys():
                                    textbutton p:
                                        text_size 16
                                        action [Function(selected_character.set_char_data, selected_character.char, p), SensitiveIf(p != selected_character.pose)]
                            
                        for g, attr in exp_previewer.layeredimages[selected_character.char][selected_character.pose].group_to_attributes.items():
                            python:
                                carrot_arrow = ">" if not attrs_vars[g] else "v"

                            textbutton carrot_arrow + " " + g:
                                text_size 16
                                action ToggleDict(attrs_vars, g, False, True)

                            if attrs_vars[g]:
                                vbox:   
                                    xoffset 20
                                    textbutton "None":
                                        text_size 16
                                        action [Function(selected_character.set_attr, g, ""), SensitiveIf("" != selected_character.attrs[g])]

                                    for a in sorted(attr):
                                        textbutton a:
                                            text_size 16
                                            action [Function(selected_character.set_attr, g, a), SensitiveIf(a != selected_character.attrs[g])]

style exposer_previewer_button_text is navigation_button_text
style exposer_previewer_button:
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
style exposer_previewer_text:
    size 18
    text_align 0.5

screen exposer_scene_prompt:
    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

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