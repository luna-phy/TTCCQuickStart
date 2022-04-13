# TTCCQuickstart
 A Toontown: Corporate Clash command-line game launcher and game updater 

 This began as a small personal project to help me log onto Corporate Clash quickly through batch scripts, to help me test Content Packs, as well as to ease multi-tooning, but slowly developed into this slightly larger project.
 
 The patching code was heavily inspired by the code graciousy developed by the [Tunetoon Project](https://github.com/DioExtreme/Tunetoon) and I am very thankful for them being able to decipher the Corporate Clash manifest API and its systems.
 
 This program's usage involves either piping commands into the 'main.py' file in the format of *account ID, toon ID, district* such as 'main.py 1 1 tesla', or by running the program with no command line at all, and running through the prompts. In the command line form, the program will never prompt the user to update, but in the normal form, each time the game is launched, the user will be prompted to update.
 
 As of now, account information is not encrypted, and is stored in the ClashLauncher.py file, and must be manually entered for the program to work. As such, do not treat this program as any sort of formal launcher.
 
### Notes
 This program assumes the default directory installation for Corporate Clash, in the AppData/Local folder, and is only tested as such, meaning that only Windows has been tested.
