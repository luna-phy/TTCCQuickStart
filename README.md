# TTCCQuickstart
 A Toontown: Corporate Clash command-line game launcher and game updater 

 This began as a small personal project to help me log onto Corporate Clash quickly through batch scripts, to help me test Content Packs, as well as to ease multi-tooning, but slowly developed into this slightly larger project.
 
 The patching code was heavily inspired by the code graciously developed by the [Tunetoon Project](https://github.com/DioExtreme/Tunetoon) and I am very thankful for them being able to decipher the Corporate Clash manifest API and its systems.
 
### Commands

| Command | Description |
| --- | --- |
| `--account` | Used to specify an account index, takes an integer from 0, up to how many accounts you've specified in `accounts.json` - 1. |
| `--toon` | Used to specify a Toon to log in with, with 0 being the top-left, 2 being the top-right, 3 being the bottom-left, and 5 being the bottom-right. |
| `--district` | Used to specify a target district to log in with. Case-insensitive. |
| `--forceupdate` | Forces the launcher to check for, and update game files, like the official launcher always does. Omission of this flag launches the game without checking for an update, which could be game-breaking. |
| `--update` | Checks for an update to game files, and prompts the user to update them, if an update exists. Does not launch the game. |
| `--updateLoop` | Does the same as `--update` but will do so forever, until the program is closed, or the game is updated. |
| `--realm` | Forces a target realm to try to log into, overriding settings from `accounts.json`. Uses default value if invalid realm is selected. |
| `--continuous` | Will not terminate program upon logout or crash, and will instead immediately log in with the initial login details. |

### Sample Usage

`python main.py --account 0 --toon 3 --district tesla`

The above command will log in using the first account specified in `accounts.json`, will use the Toon in the bottom-left slot, and will always use Tesla Tundra as the target district.

`python main.py --account 2`

The above command will log in using the third account specified in `accounts.json`, and will take the user to the main menu.

### Notes
 This program assumes the default directory installation for Corporate Clash, in the AppData/Local folder, and is only tested as such, meaning that only Windows has been tested.

 **WARNING!** This program does not provide any form of security, nor cryptography. This program leaves your usernames and passwords in plain-text within the `accounts.json` file. Please do not use this program if you intend on sharing your computer, or user, with someone else and you are concerned about account security.