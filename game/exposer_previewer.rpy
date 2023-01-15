
define total_characters = 1 
default auto_mode = True
default persistent.exp_first_run = False
default persistent.exp_advanced_first_run = False
define hide_preview_code = False
define exp_ver = 1.3

init python:
    import pygame_sdl2.scrap

    class ExPoserCharacter():
        def __init__(self):
            self.zoom_size = 0.76
            self.definition = placeholder
            self.placeholder = Placeholder("girl", text="Placeholder")
            self.ddlc_syntax = False
            self.ddlc_casual_outfit_only = False

        def parse_input_data(self):
            if self.definition.char != "Placeholder":
                if not self.ddlc_syntax:
                    try:
                        if new_can_show(self.definition.pose + " " + self.definition.input.pose_input):
                            return self.definition.pose + " " + self.definition.input.pose_input, self.zoom_size
                        else:
                            return self.placeholder, 1.0
                    except IndexError:
                        return self.placeholder, 1.0
                else:
                    if new_can_show(self.definition.char + " " + self.definition.input.pose_input):
                        return self.definition.char + " " + self.definition.input.pose_input, self.zoom_size
                    else:
                        return self.placeholder, 1.0
            else:
                return self.placeholder, 1.0
        
        def reset(self):
            self.zoom_size = 0.76
            self.definition.input.reset()
            if not self.ddlc_syntax:
                self.definition = placeholder
            else:
                self.definition = placeholder_ddlc
            self.ddlc_casual_outfit_only = False

    char1 = ExPoserCharacter()
    char2 = ExPoserCharacter()
    char3 = ExPoserCharacter()
    char4 = ExPoserCharacter()

    selected_character = char1

    def copy_line(char):
        if char.definition.char != "Placeholder":
            if not char.ddlc_syntax:
                l = "show " + char.definition.pose.strip() + " " + char.definition.input.pose_input.strip()
            else:
                l = "show " + char.definition.char + " " + char.definition.input.pose_input.strip()
            pygame_sdl2.scrap.put(pygame_sdl2.scrap.SCRAP_TEXT, l.encode("utf-8"))
            renpy.show_screen("dialog", message="Copied syntax of this character to the clipboard.", ok_action=Hide("dialog"))
        else:
            renpy.show_screen("dialog", message="Cannot copy syntax of a placeholder character.", ok_action=Hide("dialog"))

    def poser_menu_arrow_action(obj, lst, back=False):
        index = 0
        for x in range(len(lst)):
            if obj == lst[x]:
                index = x

        if back:
            return lst[index-1]
        else:
            try: return lst[index+1]
            except: return lst[0]
    
    def poser_menu_dict_action(obj, label, lst, back=False):
        # Create a new list from the keys
        all_keys = list(lst)

        # Get the current key as index
        current_index = all_keys.index(label)

        # Get the next key as index
        next_index = current_index - 1 if back else current_index + 1

        try: 
            all_keys[next_index]
            return lst[all_keys[next_index]]
        except IndexError: return lst[all_keys[0]]
    
    def apply_to_input(char):
        if not char.ddlc_syntax:
            temp = ""
            
            for key, value in char.definition.input.__dict__.items():
                if key in ["pose_input", "mpt"]: continue

                if value != "":
                    temp += value + " "
            
            char.definition.input.pose_input = temp
        else:
            if char.ddlc_casual_outfit_only:
                if not char.definition.input.pose_input[:-1].endswith("b"):
                    char.definition.input.pose_input = char.definition.input.pose_input[:-1] + "b" + char.definition.input.pose_input[-1]
                else:
                    char.definition.input.pose_input = char.definition.input.outfit
            else:
                try:
                    if char.definition.input.pose_input[-2].endswith("b"):
                        char.definition.input.pose_input = char.definition.input.pose_input[:-2] + char.definition.input.pose_input[-1]
                    else:
                        char.definition.input.pose_input = char.definition.input.outfit
                except IndexError:
                    char.definition.input.pose_input = char.definition.input.outfit
            char.definition.input.outfit = char.definition.input.pose_input
    
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

    add "bg club_day"
        
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

                textbutton "Manual Mode" action [Hide("exposer_pose_menu"), ShowMenu("exposer_previewer")]
                if selected_character.definition.char != "placeholder":
                    textbutton "Copy Pose Data" action Function(copy_line, selected_character)
                textbutton "Reset Char" action [Function(selected_character.reset), Function(apply_to_input, selected_character)]
                textbutton "Pose Menu" action If(renpy.get_screen("exposer_pose_menu"), Hide("exposer_pose_menu"), Show("exposer_pose_menu"))
                textbutton "Exit" action [Hide("exposer_pose_menu"), Return()]

            textbutton "i":
                xalign 0.99
                yalign 0.99
                action Show("dialog", message="ExPoser Previewer [exp_ver]\nCopyright © 2022 GanstaKingofSA. All rights reserved.", ok_action=Hide("dialog"))

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

                if not selected_character.ddlc_syntax:
                    hbox:
                        xoffset -10
                        xalign 0.5
                        text "Character "
                        textbutton "<" action [SetField(selected_character, "definition", poser_menu_dict_action(selected_character.definition, selected_character.definition.char, available_characters, True)), Function(apply_to_input, selected_character)]
                        null width 5
                        vbox:
                            xsize 260
                            text selected_character.definition.char xalign 0.5
                        null width 5
                        textbutton ">" action [SetField(selected_character, "definition", poser_menu_dict_action(selected_character.definition, selected_character.definition.char, available_characters)), Function(apply_to_input, selected_character)]
                else:
                    hbox:
                        xoffset -10
                        xalign 0.5
                        text "Character "
                        textbutton "<" action [SetField(selected_character, "definition", poser_menu_dict_action(selected_character.definition, selected_character.definition.char, available_ddlc_characters, True)), SetField(selected_character, "ddlc_casual_outfit_only", False), Function(apply_to_input, selected_character)]
                        null width 5
                        vbox:
                            xsize 260
                            text selected_character.definition.char.capitalize() xalign 0.5
                        null width 5
                        textbutton ">" action [SetField(selected_character, "definition", poser_menu_dict_action(selected_character.definition, selected_character.definition.char, available_ddlc_characters)), SetField(selected_character, "ddlc_casual_outfit_only", False), Function(apply_to_input, selected_character)]

                hbox:
                    text "Syntax "
                    textbutton "<" action [ToggleField(selected_character, "ddlc_syntax"), Function(selected_character.reset), Function(apply_to_input, selected_character)]
                    null width 5
                    vbox:
                        xsize 160
                        python:
                            syntax_text = "MPT/ExPoser"
                            if selected_character.ddlc_syntax:
                                syntax_text = "DDLC"
                        text syntax_text xalign 0.5
                    null width 5
                    textbutton ">" action [ToggleField(selected_character, "ddlc_syntax"), Function(selected_character.reset), Function(apply_to_input, selected_character)]

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
                        textbutton "1" action [SetVariable("selected_character", char1), SensitiveIf(selected_character != char1)]
                        if total_characters >= 2:
                            textbutton "2" action [SetVariable("selected_character", char2), SensitiveIf(selected_character != char2)]
                        if total_characters >= 3:
                            textbutton "3" action [SetVariable("selected_character", char3), SensitiveIf(selected_character != char3)]
                        if total_characters == 4:
                            textbutton "4" action [SetVariable("selected_character", char4), SensitiveIf(selected_character != char4)]

                if selected_character.definition.char != "Placeholder":
                    viewport:
                        xmaximum 420
                        ymaximum 600
                        scrollbars "vertical"
                        mousewheel True
                        has vbox

                        if selected_character.ddlc_syntax:
                            if selected_character.definition.casual != []:
                                hbox:
                                    text "Casual Outfit? "
                                    textbutton "<":
                                        action [ToggleField(selected_character, "ddlc_casual_outfit_only"), Function(apply_to_input, selected_character)]
                                    null width 5
                                    vbox:
                                        xsize 160
                                        python:
                                            casual_text = "No"
                                            if selected_character.ddlc_casual_outfit_only:
                                                casual_text = "Yes"
                                        text casual_text xalign 0.5
                                    null width 5
                                    textbutton ">": 
                                        action [ToggleField(selected_character, "ddlc_casual_outfit_only"), Function(apply_to_input, selected_character)]

                            hbox:
                                text "Pose "
                                textbutton "<":
                                    action [SetField(selected_character.definition.input, "outfit", poser_menu_arrow_action(selected_character.definition.input.outfit, (selected_character.definition.casual if selected_character.ddlc_casual_outfit_only else selected_character.definition.uniform), True)), Function(apply_to_input, selected_character)]
                                null width 5
                                vbox:
                                    xsize 20
                                    text selected_character.definition.input.outfit or "None" xalign 0.5
                                null width 5
                                textbutton ">": 
                                    action [SetField(selected_character.definition.input, "outfit", poser_menu_arrow_action(selected_character.definition.input.outfit, (selected_character.definition.casual if selected_character.ddlc_casual_outfit_only else selected_character.definition.uniform))), Function(apply_to_input, selected_character)]
                        else:
                            python:
                                def_list = selected_character.definition.__dict__.copy()
                                del def_list['pose']
                                del def_list['char']
                                del def_list['input']

                            for option, items in def_list.items():
                                null height 5

                                hbox:
                                    text option.capitalize() + " "
                                    textbutton "<":
                                        action [SetField(selected_character.definition.input, option, poser_menu_arrow_action(getattr(selected_character.definition.input, option), items, True)), Function(apply_to_input, selected_character)]
                                    null width 5
                                    vbox:
                                        xsize 20
                                        text getattr(selected_character.definition.input, option) or "None" xalign 0.5
                                    null width 5
                                    textbutton ">": 
                                        action [SetField(selected_character.definition.input, option, poser_menu_arrow_action(getattr(selected_character.definition.input, option), items)), Function(apply_to_input, selected_character)]

style exposer_previewer_button_text is navigation_button_text
style exposer_previewer_button:
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
style exposer_previewer_text:
    size 18
    text_align 0.5

screen exposer_previewer:
    tag menu
    
    style_prefix "exposer_previewer"

    add "bg club_day"

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
                xalign 0.05
                yalign 0.95
                textbutton "Switch Syntax" action [ToggleField(selected_character, "ddlc_syntax"), Function(selected_character.reset), Function(apply_to_input, selected_character)]
                textbutton "Auto Mode" action ShowMenu('new_exposer_previewer')
                textbutton "Exit" action Return()
            
            vbox:
                xalign 0.5
                yalign 0.98
                hbox:
                    python:
                        syntax_text = "MPT/ExPoser"
                        if selected_character.ddlc_syntax:
                            syntax_text = "DDLC"
                    text "Syntax: " + syntax_text xalign 0.5

                if total_characters != 1:
                    hbox:
                        xalign 0.5
                        textbutton "1" action [SetVariable("selected_character", char1), SensitiveIf(selected_character != char1)]
                        textbutton "2" action [SetVariable("selected_character", char2), SensitiveIf(selected_character != char2)]
                        if total_characters >= 3:
                            textbutton "3" action [SetVariable("selected_character", char3), SensitiveIf(selected_character != char3)]
                        if total_characters == 4:
                            textbutton "4" action [SetVariable("selected_character", char4), SensitiveIf(selected_character != char4)]
            
            vbox:
                xalign 0.95
                yalign 0.97
                hbox:
                    text "# of Chars: "
                    textbutton "1" action [SetVariable("total_characters", 1), SensitiveIf(total_characters != 1)]
                    textbutton "2" action [SetVariable("total_characters", 2), SensitiveIf(total_characters != 2)]
                    textbutton "3" action [SetVariable("total_characters", 3), SensitiveIf(total_characters != 3)]
                    textbutton "4" action [SetVariable("total_characters", 4), SensitiveIf(total_characters != 4)]                
                hbox:
                    text "Zoom Size (" + str(round(selected_character.zoom_size, 2)) + "): "
                    bar value FieldValue(selected_character, "zoom_size", 1.0) xmaximum 90
                    textbutton "R" action SetField(selected_character, "zoom_size", 0.76)
                hbox:
                    if not selected_character.ddlc_syntax:
                        text "Character: " + selected_character.definition.char
                    else:
                        text "Character: " + selected_character.definition.char.capitalize()
                    textbutton "Select" action Show("exposer_previewer_list", char=selected_character)
                hbox:
                    textbutton "Copy" action Function(copy_line, selected_character)
                    textbutton "Reset Char" action [Function(selected_character.reset), Function(apply_to_input, selected_character)]

    if not hide_preview_code:
        if selected_character.definition.char != "placeholder":
            vbox:
                xalign 0.5
                yalign 0.05
                if total_characters == 1:
                    text "Enter a ExPoser/MPT/DDLC code line."
                else: 
                    text "Enter a ExPoser/MPT/DDLC code line for this character."
            vbox:
                xalign 0.5
                yalign 0.1
                input default "" value FieldInputValue(selected_character.definition.input, "pose_input") exclude "[]\+=)(*&^%$#@!~`|{}:;\"'<,>.?/"

    on "replace" action If(persistent.exp_advanced_first_run, None, Show("dialog", message="Welcome to the manual version of {u}ExPoser Previewer!{/u}\nThis mode allows you to pose characters in real-time using your keyboard.\n\nIf you came here by mistake, click the {i}Auto Mode{/i} button to return\nto the 'Pose Menu'.", ok_action=[SetField(persistent, "exp_advanced_first_run", True), Hide("dialog")]))
    key "mouseup_3" action ToggleVariable("hide_preview_code")

screen exposer_previewer_list(char):
    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xmaximum 300
            xalign .5
            yalign .5
            spacing 30

            label _("Select a Character"):
                style "confirm_prompt"
                xalign 0.5

            viewport:
                ysize 100
                scrollbars "vertical"
                mousewheel True
                draggable True
                has vbox
                
                if not char.ddlc_syntax:
                    for x in available_characters:
                        textbutton x action [Hide("exposer_previewer_list"), SetField(selected_character, "definition", available_characters[x]), Function(apply_to_input, selected_character)]
                else:
                    for x in available_ddlc_characters:
                        textbutton x.capitalize() action [Hide("exposer_previewer_list"), SetField(selected_character, "definition", available_ddlc_characters[x]), Function(apply_to_input, selected_character)]
