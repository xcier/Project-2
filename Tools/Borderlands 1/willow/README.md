# WillowTreeBLDEnhanced

Support Borderlands GOTY Enhanced Edition for WillowTree from this sourceforge [repository](https://sourceforge.net/projects/willowtree/) 

## Getting Started

- You can download the latest realese [Here](https://github.com/Nicolas-Constanty/WillowTreeBLDEnhanced/releases)
- Extract the .zip in the folder of your choice
- Enter to your folder and execute WillTree.exe

:warning: Before using WillowTree you should make a copy of all your save! :warning:


You can find your save Here
- [User]\Documents\my games\borderlands\savedata -> Borderlands GOTY
- [User]\Documents\my games\Borderlands Game of the Year\Binaries\SaveData -> Borderlands GOTY Enhanced


WillowTree# prerelease 2.3 
-------------------------
Version 2.3  revisions were performed by matt911 and deathunt.  

WillowTree# was created by XanderChaos
WSG format research by matt911, Turk645, and XanderChaos
X360 class by DJ Shepherd 
Major revisions by JackSchitt, matt911, and da_fileserver.
Additional  ideas and code contributions by CK Y and mphjens.

WillowTree# is an open source project.  Visit the development site at willowtree.sourceforge.net.
-------------------------
Update prerelease v2.3.3
- Rewrite bank objects parsing
- Loading and Saving should work now

-------------------------
Update prerelease v2.3.1
- Fixed loading of Borderlands GOTY Enhanced
- Fixed saving of Borderlands GOTY Enhanced
- Refacto of Item lists and Weapon lists with two class Item and Weapon (Items = List(Item) and Weapons = List(Weapon)) 
- Change Unknow2 to Head

-------------------------
Update prerelease v2.3.0
- WillowTree# code is now officially licensed under the GNU General Public License version 3.
- Complete user interface conversion of WillowTree# to remove the DotNetBar component library.
- Improved item naming code so the names look more like in the game.
- New options are available to display the item or weapon level or rarity in the lists.
- Lists can be colorized according to rarity.  It is disabled by default, but you can enable it in the options menu.
- Item, weapon, and locker lists can now be sorted  and categorized.  Press F1 to select a sorting scheme and F2 to select the sorting tree depth.
- Modified error handling to makes it easier to detect and debug problems in some instances.
- Quality and level now have three options for editing and viewing.  You can use the sliders to edit the level or view and modify the level index (which is the level + 2) directly in a signed integer or signed hexadecimal edit box.
- The user interface now displays and supports the full 32-bit level for Scorpio weapons
- The part selector can now track the part list automatically.
- Part information window added to the item panel.
- More options are available for importing quests, echoes, and locations.
- Improved weapon calculations.  The numbers should be more accurate now.  The percentages you see are not the same as the numbers in the game because the numbers in the game are wrong as far as I can tell.
- Fixes to X360 DLL library prevent hanging when trying to load an Xbox save.
- Fixes to X360.DLL library prevent the WillowTree icon from becoming a tiger icon in some Xbox 360 savegames.
- Fixed a bug that would cause WT# to fail to load  if installed in a path that contains a folder named Data.
- Fixed several bugs relating to inventory being organized by its name in WillowTree#. The most obvious of these was that exporting items to a file would make all items with the same name improperly assume the stats of the first such item.
- Lots of internal code reorganization in WillowTreeMain.cs and WillowSaveGame.cs that is not visible to the end user.  Many variables and functions have changed names, been removed, or been replaced.
- Fixed a bug preventing changing the current location in savegames.
- Updated location data to include more useful descriptions of each location.  Locations in parenthesis have no teleporter and cannot be teleported to.
- Handling is modified so WT# can properly process any arbitrary number of quest lists and echo lists.
- All user interface elements should be fixed size and independent of the Windows system settings now so increasing the Windows display DPI setting will no longer disrupt the layout of the WT# window by causing menus to cover over other elements.
- Multple-selection support has been added to trees so you can copy, delete, or move multiple items at once.  Hold ctrl or shift as you click your mouse as in other Windows applications.
- The way files are used has been revised.  There is more caching in memory so the data will not be read from disk as often.
- WT# will now offer to repair some corrupt savegames it could not load otherwise.
- WT# will now offer to strip raw data from savegames it could not convert to another machine-byte-order otherwise.

Update v2.2.1
- Fixed a bug with Xbox saves in 2.2 not working when you used the Save button (Save As worked fine)
- Changed the UI interface for the Xbox ID a bit so it will show you the ID
- Changing save format now disables the Save button and will force you to use Save As
- Changing format to PS3 now explains that you will need other files to go with the save file

Update v2.2.0
- Savegame conversion has been implemented.  You can now write most saves as PC, PS3, or Xbox 360.
- Fixed inability to load Xbox 360 savegames at all in version 2.1 and 2.1.1 because of missing resource file.
- Window title updates now so you can look at it to know which character you are editing
- Fixed a bug in the item level/quality handling that resulted in Scorpio weapons being corrupted in all 2.1 revisions.

Update v2.1.1:
- Rewrote string handling to work with non-English strings.  A hotfix version 2.1.0.40 broke the PS3/Xbox string handling.  This fixes that.

Update v2.1.0:
- Complete rewrite of the DLC block load/save code
- Reviewed, tested, and revised all the rest of the savegame read/write code.  Should have fixed most remaining load/save issues.
- Fixed bank size corruption when there was only one echo log in a save.
- Locker saves item level, quality, and ammo now.
- Locker names will not change as much when you shut down and reload.
- Clipboard and file import/export  gets validated more so you shouldn't cause a crash with invalid data as easily.
- Lots of fixes to the  import/export/insert functions in the weapon, items, and locker tab of the UI.  Added some slider controls like the weapon and item panel for consistency.

Update v2.0.0:
- Moved the entire project from Multimedia Fusion to C#.
- New, user-friendly GUI.
- Merged Weapons Workshop into WillowTree.
- Skills, Quests, Ammo Pools, Echo Logs, and Locations are now fully editable. You can now add, edit, and remove items from each of these sections.
- More values are available to edit.
- Automatic backups of saves.
- Added the WillowTree Locker to keep track off weapons and items between saves. Weapons/Items can be given custom names, commented on, and rated. 

Update v1.2.2:
- Fixed the PC version file loading issue. 

Update v1.2.1:
- Slightly changed rebuilding code. Hopefully less bugs.
- Removed "Delete Item/Weapon" as it isn't working correctly.
- Added code to adjust important hash block info on the 360 version.
(Only Weapons Workshop was altered) 

Update v1.2.0:
- Added the new "Weapons Workshop" mode. It specificly edits weapons and items. Unlike the normal WillowTree mode, here you can add/remove/duplicate new weapons and items! It also includes a full list of parts (rather than the last version's limited list). Thanks to Turk there is a check on ItemGrades to make sure that you weapon won't revert to level 0.

Update v1.1.1:
- Added support for new DLC quests. 

Update v1.1.0:
- New organized decompiling process.
- Added an editor for the multiple parts of the save. It can quickly edit weapons, items, quests, player info, character colors, name, skills, locations, and invintory info.
- Added weapon and item importing/exporting from files or from the clipboard.
- Built-in parts swapper.
- Number of bugs fixed.
- PC support added. 

Update v1.0.1:
- Fixes a few minor bugs.
- Added PS3 save support.

## Licence
WillowTree# is free software: you can redistribute and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

WillowTree# uses a modified version of the X360 library which is 
subject to the GNU General Public License version 3 along with
additional terms that are listed in X360.COPYING.TXT.

Source code to both WillowTree# and the modified version of X360.DLL
are available at http://willowtree.sourceforge.net.

WillowTree# is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with WillowTree# (usually in COPYING.TXT).  If not, see 
<http://www.gnu.org/licenses/>.
