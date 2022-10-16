# ExPoser Previewer
> ExPoser Previewer is only supported on Ren'Py 7 and 8.

ExPoser Previewer is a DDLC pose previewing tool that allows modders to pose and express their characters in real-time within DDLC. 

With support for DDLC poses and expressions, and Mood Pose Tool (MPT) ones (including ExPoser poses), there are endless possibilities to pose in DDLC and ExPoser Previewer allows you to view all of them for not just each of the doki's, but including other characters with a custom definition file.

## Features
- Preview any pose and expression from DDLC to MPT (including ExPoser ones) in real-time.
- Copy pose code from ExPoser Previewer to your mod.
- Manual Mode: A menu where you can type any DDLC, MPT or ExPoser pose and expression for viewing.
- Auto Mode: A menu where you can adjust poses and expressions via a list of pose/expression items.
- Custom Definitions: Make a custom definition file for another character and be able to pose/express them in ExPoser Previewer for you or everyone else.

## Installation
> Make sure you have MPT **or** MPT + ExPoser installed in your mod before doing this.
1. Download ExPoser Previewer from [here](https://github.com/GanstaKingofSA/ExPoser-Previewer/releases).
2. Drop the contents from the ZIP file to your mod.
3. Open `screens.rpy` and add this line somewhere in the navigation screen
   ```py
   textbutton _("ExP Previewer") action If(auto_mode, ShowMenu("new_exposer_previewer"), ShowMenu("exposer_previewer"))
   ```
4. Launch DDLC.
5. Click *ExP Previewer* and get to posing.

## What difference does this have to the Doki Doki Posing Tool site?
The Posing Tool site from what I know only supports DDLC positions and a few characters that are outside the base game which only supports DDLC syntax. ExPoser Previewer allows MPT/ExPoser syntax and a finite amount of possibilities to pose/express the main girls and other characters via a custom definition file.

## Does this support the old Agent Gold Pose Tool?
No. ExPoser Previewer is only designed for the most recent tools currently in DDLC modding which is DDLC itself, MPT and ExPoser.

## How do I make my own definition file for a OC I made/edit a definition file to add more stuff?
Follow [this](./ExPoser%20Previewer%20Documentation.pdf) guide on how to make your own definition file for your own OC/edit to add more content to a existing one.

Copyright © 2022 GanstaKingofSA. All rights reserved.

MPT, Mood Pose Tool is the property of u/chronoshag and the MPT team. No MPT assets are provided in ExPoser Previewer.

ExPoser (ExP) is the property of GanstaKingofSA.

DDLC, the DDLC posing code are property of Team Salvato.