# ExPoser Previewer
> ExPoser Previewer is only supported on Ren'Py 7 and 8.

ExPoser Previewer is a DDLC pose previewing tool that allows modders to pose and express their characters in real-time within DDLC. 

With support for all DDLC poses and expressions, including Mood Pose Tool (MPT)/ExPoser (ExP) ones, there are endless possibilities to pose in DDLC. With ExPoser Previewer, this tool allows you to view all of them for not just each of the doki's, but including other characters as well with a auto-generated definition file.

## Features
- Preview any pose and expression from DDLC to MPT/ExPoser in real-time.
- Copy pose code from ExPoser Previewer to your mod.
- Manual Mode: A menu where you can type any DDLC, MPT/ExPoser pose and expression for viewing.
- Auto Mode: A menu where you can adjust poses and expressions via a list of pose/expression items.
- Custom Definitions: Generate a custom definition file automatically for another character in your mod and be able to pose/express them in ExPoser Previewer for you or everyone else by sharing the definition files.
   > Generation of new character definition files or edits to a existing character (addition/removal), requires *config.developer* to be enabled in `definitions/definitions.rpy` (`definitions.rpy` for old template layouts [MAS (0.1.0 - 1.1.2) | Mod Template 2.0 (2.1.0 - 4.0.2)]) and a game restart to compile the generated RPY file.

## Installation
> Make sure you have MPT **or** MPT + ExPoser installed in your mod before doing this.
1. Download ExPoser Previewer from [here](https://github.com/GanstaKingofSA/ExPoser-Previewer/releases).
2. Drop the contents from the ZIP file to your mod.
3. Open `screens.rpy` and add this line somewhere in the navigation screen
   ```py
   textbutton _("ExP Previewer") action ShowMenu("new_exposer_previewer")
   ```
4. Launch DDLC.
5. Click *ExP Previewer* and get to posing.

## What difference does this have to the Doki Doki Posing Tool site?
The Posing Tool site from what I know only supports the Doki cast and a few other characters that only supports DDLC syntax. ExPoser Previewer supports both DDLC and MPT/ExPoser syntax with a finite amount of possibilities of pose/express any character which supports MPT/ExPoser and/or DDLC syntax.

## Does this support the old Agent Gold Pose Tool?
No. ExPoser Previewer was designed to support DDLC and MPT/ExPoser syntax. This pose tool is obsolete and should be replaced with MPT + ExPoser.

Copyright © 2022 GanstaKingofSA. All rights reserved.

Mood Pose Tool (MPT) is the property of u/chronoshag and the MPT team. No MPT assets are provided in ExPoser Previewer.

ExPoser (ExP) is the property of GanstaKingofSA.

DDLC, the DDLC posing code (DDLC syntax) are the property of Team Salvato.