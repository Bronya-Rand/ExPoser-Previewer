# ExPoser Previewer
> ExPoser Previewer is only supported on Ren'Py 7 and 8.

ExPoser Previewer is a DDLC pose previewing tool that allows modders to pose and express their characters in real-time within DDLC. 

With support for all expressions from DDLC to Mood Pose Tool (MPT) and ExPoser (ExP), there are endless possibilities to pose in DDLC. With ExPoser Previewer, this tool allows you to view all of them for not just each of the doki's, but including other characters as well!

## Features
- Preview any pose and expression from MPT, ExPoser and DDLC in real-time.
- Copy pose code from ExPoser Previewer to your mod.
- Change bg scenery.
- Mulitple character posing.
- Dynamic character fetching (characters are auto-defined).
- Dynamic scaling support for 1080p+*
   > Just to get this out the way, if you just scaled the DDLC sprites by 2 times, you are *not* 1080p. You are more 1440p in this regard. Adjust the math in `calculate_dsr` to adjust for this.

## Installation
> Make sure you have MPT **or** MPT + ExPoser installed in your mod before doing this.

> Make sure to remove or change the `ExP Previewer` textbutton if you are upgrading to 2.0+. The buttons prior do not work anymore.
1. Download ExPoser Previewer from [here](https://github.com/GanstaKingofSA/ExPoser-Previewer/releases).
2. Drop the contents from the ZIP file to your mod.
4. Launch DDLC.
5. Press *Shift+F5* and get to posing.
    > Alternatively if you want the button mode back use the following.
    > ```py
    > textbutton "ExP Previewer" action ShowMenu("new_exposer_previewer")
    > ```

## What difference does this have to the Doki Doki Posing Tool website?
There are major differences between ExPoser Previewer and the Doki Doki Posing Tool website.
1. The Doki Doki Posing Tool website lacks LayeredImage support.
   > The Doki Doki Posing Tool website is only designed to show characters that have DDLC syntax. ExPoser Previewer shows not only shows DDLC syntax but LayeredImage syntax from either MPT or ExPoser as well.
2. The Doki Doki Posing Tool website supports limited amount of characters.
   > The Doki Doki Posing Tool website is dependent on the characters the creator has gotten permission from on their website. ExPoser Previewer allows you to see any character that you want as long as they are defined, and are a valid character.

## What difference does this have to Elkcarow's Expreviewer?
They are both identical in some degree. Implementation is different though. A few differences are the following.
1. Expreviewer requires that characters are manually defined in the source file.
   > ExPoser Previewer does this automatically at runtime (this also means no more `X_pose_defs.rpy` files anymore.)
2. Expreviewer lacks custom background support.
   > ExPoser Previewer displays all backgrounds in the game that are tagged as `bg`. Additionally you may also load a custom background file by it's path name or another variable name.
3. Expreviewer lacks DDLC Syntax Mode.
   > Expreviewer is only focused on LayeredImage syntax from either MPT or ExPoser. ExPoser Previewer shows not only LayeredImage syntax but DDLC syntax as well.

There might be a few more differences but thats the major three I see. Obviously ExPoser Previewer is coded differently and might not be clean compared to Expreviewer but it gets the job done.

## Does this support the old Agent Gold Pose Tool?
No. ExPoser Previewer was designed to support DDLC and MPT/ExPoser syntax. This pose tool is obsolete and should be replaced with MPT + ExPoser.

## Credits
- Elckarow - [exp_parser.rpy](./game/exp_parser.rpy) initial code [1.0-1.2].

Copyright © 2022-2023 bronya_rand. All rights reserved.

Mood Pose Tool (MPT) is the property of u/chronoshag and the MPT team. No MPT assets are provided in ExPoser Previewer.

ExPoser (ExP) is the property of bronya_rand.

DDLC, the DDLC posing code (DDLC syntax) are the property of Team Salvato.