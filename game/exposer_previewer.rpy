
define total_characters = 1 
default auto_mode = True
default persistent.exp_first_run = False
default persistent.exp_advanced_first_run = False
define hide_preview_code = False

init python:
    import pygame_sdl2.scrap
    import re

    class ExPoserCharacter:
        def __init__(self):
            self.pose_input = ""
            self.zoom_size = 0.76
            self.definition = placeholder
            self.placeholder = Placeholder("girl", text="Placeholder")
            self.allow_exposer_syntax = True
            self.ddlc = True
            self.ddlc_pose = 1
            self.ddlc_casual = False
            self.ddlc_expression = "a"
            self.mpt_pose = "base" if self.allow_exposer_syntax else "forward"
            self.mpt_outfit = "uniform"
            self.mpt_mood = "neut"
            self.mpt_head = ""
            self.mpt_blush = ""
            self.mpt_left_pose = ""
            self.mpt_right_pose = ""
            self.mpt_nose = ""
            self.mpt_mouth = ""
            self.mpt_eye = ""
            self.mpt_eyebrow = ""
            self.mpt_allow_special_scream = False
            self.mpt_special = "s_scream"

        def parse_input_data(self):
            if self.definition.char != "placeholder":
                try:
                    if new_can_show(self.definition.char + " " + self.pose_input):
                        return self.definition.char + " " + self.pose_input, self.zoom_size
                    else:
                        return self.placeholder, 1.0
                except IndexError:
                    return self.placeholder, 1.0
            else:
                return self.placeholder, 1.0
        
        def reset(self):
            self.pose_input = ""
            self.zoom_size = 0.76
            self.definition = placeholder
            self.allow_exposer_syntax = False
            self.ddlc_pose = 1
            self.ddlc_casual = False
            self.ddlc_expression = "a"
            self.mpt_pose = "base" if self.allow_exposer_syntax else "forward"
            self.mpt_outfit = "uniform"
            self.mpt_mood = "neut"
            self.mpt_head = ""
            self.mpt_blush = ""
            self.mpt_left_pose = ""
            self.mpt_right_pose = ""
            self.mpt_nose = ""
            self.mpt_mouth = ""
            self.mpt_eye = ""
            self.mpt_eyebrow = ""
            self.mpt_allow_special_scream = False

    char1 = ExPoserCharacter()
    char2 = ExPoserCharacter()
    char3 = ExPoserCharacter()
    char4 = ExPoserCharacter()

    selected_character = char1

    def copy_line(char):
        if char.definition.char != "placeholder":
            l = "show " + char.definition.char.strip() + " " + char.pose_input.strip()
            pygame_sdl2.scrap.put(pygame_sdl2.scrap.SCRAP_TEXT, l.encode("utf-8"))
            if not char.ddlc and char.allow_exposer_syntax:
                renpy.show_screen("dialog", message="Copied syntax of this character to the clipboard.\n{b}NOTE:{/b}The syntax created only works for the {u}ExPoser{/u} pose tool.", ok_action=Hide("dialog"))
            else:
                renpy.show_screen("dialog", message="Copied syntax of this character to the clipboard.", ok_action=Hide("dialog"))
        else:
            renpy.show_screen("dialog", message="Cannot copy syntax of a Placeholder character.", ok_action=Hide("dialog"))

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
        if char.definition.ddlc and char.ddlc:
            if char.ddlc_casual:
                char.pose_input = str(char.ddlc_pose) + "b" + char.ddlc_expression
            else:
                char.pose_input = str(char.ddlc_pose) + char.ddlc_expression
        else:
            if char.mpt_pose == "base" and not char.allow_exposer_syntax:
                char.mpt_pose = "turned"
            elif char.definition.supports_exposer and (char.mpt_pose == "forward" or char.mpt_pose == "turned") and char.allow_exposer_syntax:
                char.mpt_pose = "base"

            char.pose_input = char.mpt_pose + " " + char.mpt_outfit + " " + char.mpt_mood
            if char.mpt_allow_special_scream:
                for x in [char.mpt_blush, char.mpt_left_pose, char.mpt_right_pose, char.mpt_nose, char.mpt_mouth, char.mpt_eye, char.mpt_eyebrow, char.mpt_special]:
                    if x:
                        char.pose_input += " " + x
            elif char.mpt_head:
                for x in [char.mpt_blush, char.mpt_left_pose, char.mpt_right_pose, char.mpt_head, char.mpt_nose, char.mpt_mouth, char.mpt_eye, char.mpt_eyebrow]:
                    if x:
                        char.pose_input += " " + x
            else:
                for x in [char.mpt_blush, char.mpt_left_pose, char.mpt_right_pose, char.mpt_nose, char.mpt_mouth, char.mpt_eye, char.mpt_eyebrow]:
                    if x:
                        char.pose_input += " " + x
    
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
                    xalign 0.5
                    text "Character "
                    textbutton "<" action [SetField(selected_character, "definition", poser_menu_dict_action(selected_character.definition, selected_character.definition.char, available_characters, True)), Function(apply_to_input, selected_character)]
                    null width 5
                    vbox:
                        xsize 260
                        text selected_character.definition.char.capitalize() xalign 0.5
                    null width 5
                    textbutton ">" action [SetField(selected_character, "definition", poser_menu_dict_action(selected_character.definition, selected_character.definition.char, available_characters)), Function(apply_to_input, selected_character)]
                
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

                if selected_character.definition.char != "placeholder":
                    if selected_character.definition.ddlc:
                        hbox:
                            text "Syntax "
                            textbutton "<" action [ToggleField(selected_character, "ddlc"), Function(apply_to_input, selected_character)]
                            null width 5
                            vbox:
                                xsize 160
                                python:
                                    syntax_text = "MPT/ExPoser"
                                    if selected_character.ddlc:
                                        syntax_text = "DDLC"
                                text syntax_text xalign 0.5
                            null width 5
                            textbutton ">" action [ToggleField(selected_character, "ddlc"), Function(apply_to_input, selected_character)]
                    
                    if selected_character.ddlc:
                        hbox:
                            text "Pose # "
                            textbutton "<" action [SetField(selected_character, "ddlc_pose", poser_menu_arrow_action(selected_character.ddlc_pose, selected_character.definition.ddlc_def.ddlc_poses, True)), Function(apply_to_input, selected_character)]
                            null width 5
                            vbox:
                                xsize 20
                                text str(selected_character.ddlc_pose) xalign 0.5
                            null width 5
                            textbutton ">" action [SetField(selected_character, "ddlc_pose", poser_menu_arrow_action(selected_character.ddlc_pose, selected_character.definition.ddlc_def.ddlc_poses)), Function(apply_to_input, selected_character)]

                        hbox:
                            text "Casual Outfit? "
                            vbox:
                                xsize 50
                                python:
                                    casual_text = "Yes"
                                    if not selected_character.ddlc_casual:
                                        casual_text = "No"

                                text casual_text xalign 0.5
                            null width 5
                            textbutton ">" action [ToggleField(selected_character, "ddlc_casual"), Function(apply_to_input, selected_character)]

                        hbox:
                            text "Expression "
                            textbutton "<" action [SetField(selected_character, "ddlc_expression", poser_menu_arrow_action(selected_character.ddlc_expression, selected_character.definition.ddlc_def.ddlc_special_expressions if selected_character.ddlc_pose in selected_character.definition.ddlc_def.ddlc_special_pose else selected_character.definition.ddlc_def.ddlc_expressions, True)), Function(apply_to_input, selected_character)]
                            null width 5
                            vbox:
                                xsize 20
                                text selected_character.ddlc_expression xalign 0.5
                            null width 5
                            textbutton ">" action [SetField(selected_character, "ddlc_expression", poser_menu_arrow_action(selected_character.ddlc_expression, selected_character.definition.ddlc_def.ddlc_special_expressions if selected_character.ddlc_pose in selected_character.definition.ddlc_def.ddlc_special_pose else selected_character.definition.ddlc_def.ddlc_expressions)), Function(apply_to_input, selected_character)]
                    else:
                        if selected_character.definition.supports_exposer:
                            hbox:
                                text "Allow ExPoser Syntax? "
                                vbox:
                                    xsize 50
                                    python:
                                        exposer_text = "Yes"
                                        if not selected_character.allow_exposer_syntax:
                                            exposer_text = "No"

                                    text exposer_text xalign 0.5
                                null width 5
                                textbutton ">" action [ToggleField(selected_character, "allow_exposer_syntax"), Function(apply_to_input, selected_character)]

                        hbox:
                            text "Pose "
                            textbutton "<" action [SetField(selected_character, "mpt_pose", poser_menu_arrow_action(selected_character.mpt_pose, (selected_character.definition.exposer_poses if selected_character.allow_exposer_syntax else selected_character.definition.poses) + selected_character.definition.second_poses, True)), Function(apply_to_input, selected_character)]
                            null width 5
                            vbox:
                                xsize 20
                                text selected_character.mpt_pose xalign 0.5
                            null width 5
                            textbutton ">" action [SetField(selected_character, "mpt_pose", poser_menu_arrow_action(selected_character.mpt_pose, (selected_character.definition.exposer_poses if selected_character.allow_exposer_syntax else selected_character.definition.poses) + selected_character.definition.second_poses)), Function(apply_to_input, selected_character)]

                        hbox:
                            text "Outfit "
                            textbutton "<" action [SetField(selected_character, "mpt_outfit", poser_menu_arrow_action(selected_character.mpt_outfit, selected_character.definition.outfits, True)), Function(apply_to_input, selected_character)]
                            null width 5
                            vbox:
                                xsize 20
                                text selected_character.mpt_outfit xalign 0.5
                            null width 5
                            textbutton ">" action [SetField(selected_character, "mpt_outfit", poser_menu_arrow_action(selected_character.mpt_outfit, selected_character.definition.outfits)), Function(apply_to_input, selected_character)]

                        hbox:
                            text "Mood "
                            textbutton "<" action [SetField(selected_character, "mpt_mood", poser_menu_arrow_action(selected_character.mpt_mood, selected_character.definition.second_moods if selected_character.mpt_pose in selected_character.definition.second_poses else selected_character.definition.moods, True)), Function(apply_to_input, selected_character)]
                            null width 5
                            vbox:
                                xsize 20
                                text selected_character.mpt_mood xalign 0.5
                            null width 5
                            textbutton ">" action [SetField(selected_character, "mpt_mood", poser_menu_arrow_action(selected_character.mpt_mood, selected_character.definition.second_moods if selected_character.mpt_pose in selected_character.definition.second_poses else selected_character.definition.moods)), Function(apply_to_input, selected_character)]

                        if selected_character.definition.head:
                            hbox:
                                text "Head "
                                textbutton "<" action [SetField(selected_character, "mpt_head", poser_menu_arrow_action(selected_character.mpt_head, selected_character.definition.head, True)), Function(apply_to_input, selected_character)]
                                null width 5
                                vbox:
                                    xsize 20
                                    text selected_character.mpt_head or "Default" xalign 0.5
                                null width 5
                                textbutton ">" action [SetField(selected_character, "mpt_head", poser_menu_arrow_action(selected_character.mpt_head, selected_character.definition.head)), Function(apply_to_input, selected_character)]

                        hbox:
                            text "Blushes "
                            textbutton "<" action [SetField(selected_character, "mpt_blush", poser_menu_arrow_action(selected_character.mpt_blush, selected_character.definition.second_blushes if selected_character.mpt_pose in selected_character.definition.second_poses else selected_character.definition.blushes, True)), Function(apply_to_input, selected_character)]
                            null width 5
                            vbox:
                                xsize 20
                                text selected_character.mpt_blush or "Default" xalign 0.5
                            null width 5
                            textbutton ">" action [SetField(selected_character, "mpt_blush", poser_menu_arrow_action(selected_character.mpt_blush, selected_character.definition.second_blushes if selected_character.mpt_pose in selected_character.definition.second_poses else selected_character.definition.blushes)), Function(apply_to_input, selected_character)]

                        if selected_character.mpt_pose not in selected_character.definition.second_poses:
                            hbox:
                                text "Left Pose "
                                textbutton "<" action [SetField(selected_character, "mpt_left_pose", poser_menu_arrow_action(selected_character.mpt_left_pose, selected_character.definition.left_poses, True)), Function(apply_to_input, selected_character)]
                                null width 5
                                vbox:
                                    xsize 20
                                    text selected_character.mpt_left_pose or "Default" xalign 0.5
                                null width 5
                                textbutton ">" action [SetField(selected_character, "mpt_left_pose", poser_menu_arrow_action(selected_character.mpt_left_pose, selected_character.definition.left_poses)), Function(apply_to_input, selected_character)]

                            hbox:
                                text "Right Pose "
                                textbutton "<" action [SetField(selected_character, "mpt_right_pose", poser_menu_arrow_action(selected_character.mpt_right_pose, selected_character.definition.right_poses, True)), Function(apply_to_input, selected_character)]
                                null width 5
                                vbox:
                                    xsize 20
                                    text selected_character.mpt_right_pose or "Default" xalign 0.5
                                null width 5
                                textbutton ">" action [SetField(selected_character, "mpt_right_pose", poser_menu_arrow_action(selected_character.mpt_right_pose, selected_character.definition.right_poses)), Function(apply_to_input, selected_character)]
                        
                        if selected_character.definition.head and selected_character.mpt_head:
                            hbox:
                                text "Noses "
                                textbutton "<" action [SetField(selected_character, "mpt_nose", poser_menu_arrow_action(selected_character.mpt_nose, selected_character.definition.head_noses, True)), Function(apply_to_input, selected_character)]
                                null width 5
                                vbox:
                                    xsize 20
                                    text selected_character.mpt_nose or "Default" xalign 0.5
                                null width 5
                                textbutton ">" action [SetField(selected_character, "mpt_nose", poser_menu_arrow_action(selected_character.mpt_nose, selected_character.definition.head_noses)), Function(apply_to_input, selected_character)]

                            hbox:
                                text "Mouths "
                                textbutton "<" action [SetField(selected_character, "mpt_mouth", poser_menu_arrow_action(selected_character.mpt_mouth, selected_character.definition.head_mouths, True)), Function(apply_to_input, selected_character)]
                                null width 5
                                vbox:
                                    xsize 20
                                    text selected_character.mpt_mouth or "Default" xalign 0.5
                                null width 5
                                textbutton ">" action [SetField(selected_character, "mpt_mouth", poser_menu_arrow_action(selected_character.mpt_mouth, selected_character.definition.head_mouths)), Function(apply_to_input, selected_character)]

                            hbox:
                                text "Eyes "
                                textbutton "<" action [SetField(selected_character, "mpt_eye", poser_menu_arrow_action(selected_character.mpt_eye, selected_character.definition.head_eyes, True)), Function(apply_to_input, selected_character)]
                                null width 5
                                vbox:
                                    xsize 20
                                    text selected_character.mpt_eye or "Default" xalign 0.5
                                null width 5
                                textbutton ">" action [SetField(selected_character, "mpt_eye", poser_menu_arrow_action(selected_character.mpt_eye, selected_character.definition.head_eyes)), Function(apply_to_input, selected_character)]

                            hbox:
                                text "Eyebrows "
                                textbutton "<" action [SetField(selected_character, "mpt_eyebrow", poser_menu_arrow_action(selected_character.mpt_eyebrow, selected_character.definition.head_eyebrows, True)), Function(apply_to_input, selected_character)]
                                null width 5
                                vbox:
                                    xsize 20
                                    text selected_character.mpt_eyebrow or "Default" xalign 0.5
                                null width 5
                                textbutton ">" action [SetField(selected_character, "mpt_eyebrow", poser_menu_arrow_action(selected_character.mpt_eyebrow, selected_character.definition.head_eyebrows)), Function(apply_to_input, selected_character)]
                        else:
                            hbox:
                                text "Noses "
                                textbutton "<" action [SetField(selected_character, "mpt_nose", poser_menu_arrow_action(selected_character.mpt_nose, selected_character.definition.second_noses if selected_character.mpt_pose in selected_character.definition.second_poses else selected_character.definition.noses, True)), Function(apply_to_input, selected_character)]
                                null width 5
                                vbox:
                                    xsize 20
                                    text selected_character.mpt_nose or "Default" xalign 0.5
                                null width 5
                                textbutton ">" action [SetField(selected_character, "mpt_nose", poser_menu_arrow_action(selected_character.mpt_nose, selected_character.definition.second_noses if selected_character.mpt_pose in selected_character.definition.second_poses else selected_character.definition.noses)), Function(apply_to_input, selected_character)]

                            hbox:
                                text "Mouths "
                                textbutton "<" action [SetField(selected_character, "mpt_mouth", poser_menu_arrow_action(selected_character.mpt_mouth, selected_character.definition.second_mouths if selected_character.mpt_pose in selected_character.definition.second_poses else selected_character.definition.mouths, True)), Function(apply_to_input, selected_character)]
                                null width 5
                                vbox:
                                    xsize 20
                                    text selected_character.mpt_mouth or "Default" xalign 0.5
                                null width 5
                                textbutton ">" action [SetField(selected_character, "mpt_mouth", poser_menu_arrow_action(selected_character.mpt_mouth, selected_character.definition.second_mouths if selected_character.mpt_pose in selected_character.definition.second_poses else selected_character.definition.mouths)), Function(apply_to_input, selected_character)]

                            hbox:
                                text "Eyes "
                                textbutton "<" action [SetField(selected_character, "mpt_eye", poser_menu_arrow_action(selected_character.mpt_eye, selected_character.definition.second_eyes if selected_character.mpt_pose in selected_character.definition.second_poses else selected_character.definition.eyes, True)), Function(apply_to_input, selected_character)]
                                null width 5
                                vbox:
                                    xsize 20
                                    text selected_character.mpt_eye or "Default" xalign 0.5
                                null width 5
                                textbutton ">" action [SetField(selected_character, "mpt_eye", poser_menu_arrow_action(selected_character.mpt_eye, selected_character.definition.second_eyes if selected_character.mpt_pose in selected_character.definition.second_poses else selected_character.definition.eyes)), Function(apply_to_input, selected_character)]

                            hbox:
                                text "Eyebrows "
                                textbutton "<" action [SetField(selected_character, "mpt_eyebrow", poser_menu_arrow_action(selected_character.mpt_eyebrow, selected_character.definition.second_eyebrows if selected_character.mpt_pose in selected_character.definition.second_poses else selected_character.definition.eyebrows, True)), Function(apply_to_input, selected_character)]
                                null width 5
                                vbox:
                                    xsize 20
                                    text selected_character.mpt_eyebrow or "Default" xalign 0.5
                                null width 5
                                textbutton ">" action [SetField(selected_character, "mpt_eyebrow", poser_menu_arrow_action(selected_character.mpt_eyebrow, selected_character.definition.second_eyebrows if selected_character.mpt_pose in selected_character.definition.second_poses else selected_character.definition.eyebrows)), Function(apply_to_input, selected_character)]

                        if selected_character.mpt_pose not in selected_character.definition.second_poses:
                            vbox:
                                hbox:
                                    text "Enable Special Scream?"
                                    vbox:
                                        xsize 50
                                        python:
                                            special_scream_text = "Yes"
                                            if not selected_character.mpt_allow_special_scream:
                                                special_scream_text = "No"

                                        text special_scream_text xalign 0.5
                                    null width 5
                                    textbutton ">" action [ToggleField(selected_character, "mpt_allow_special_scream"), Function(apply_to_input, selected_character)]

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
                textbutton "Auto Mode" action ShowMenu('new_exposer_previewer')
                textbutton "Exit" action Return()
            
            if total_characters != 1:
                hbox:
                    xalign 0.5
                    yalign 0.99
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
                    text "Character: " + str(selected_character.definition.char.capitalize())
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
                input default "" value FieldInputValue(selected_character, "pose_input") exclude "[]\+=)(*&^%$#@!~`|{}:;\"'<,>.?/"

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

                for x in available_characters:
                    textbutton x.capitalize() action [Hide("exposer_previewer_list"), SetField(selected_character, "definition", available_characters[x]), Function(apply_to_input, selected_character)]
