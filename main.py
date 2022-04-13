from ClashLauncher import ClashLauncher
from ClashPatcher import ClashPatcher

import sys

if len(sys.argv) > 1:
    print('Logging in through Command-Line, bypassing update check')
    launcher = ClashLauncher(*sys.argv[1:])
    launcher.connect()
    sys.exit()

patcher = ClashPatcher()
updated = False

userInput: str = ''
while not userInput.lower() == 'quit':
    userInput: str = input('>> ')
    if userInput.lower() == 'login':
        if not updated:
            print('Check for Game Updates?')
            userInput: str = input('Y/N >> ')
            
            if userInput.lower() == 'y':   
                if patcher.isGameUpdated():
                    updated = True
                    print('Game files are fully up-to-date.')
                else:
                    print('Game files require an update. Update them now?')
                    userInput: str = input('Y/N >> ')
                    if userInput.lower() == 'y':
                        updated = True
                        patcher.run()
                        print('Game has been updated.')
        
        acc: str = input('Account ID >> ')
        if not acc.isnumeric():
            print('Invalid account ID format.')
            continue
        
        toon: str = input('Toon ID >> ')
        if not toon.isnumeric():
            toon = '-1'

        district: str = input('Target District >> ')

        launcher = ClashLauncher(acc, toon, district)

        while launcher.connect():
            print('Reconnect?')
            userInput = input('Y/N >> ')
            if not userInput.lower() == 'y':
                break
    elif userInput.lower() in {'update', 'patch'}:
        print('Checking for update...')
        if not updated and not patcher.isGameUpdated():
            print('Local files are old, update them?')
            userInput: str = input('Y/N >> ')
            
            if userInput.lower() == 'y':
                updated = True
                patcher.run()
                print('Game has been updated.')
        else:
            updated = True
            print('Game is already up-to-date.')
    elif userInput.lower() == 'help':
        print('Corporate Clash Launcher by luna#4811\n\tlogin - Login to the game.\n\tpatch - Update game files.\n\thelp - Display this text.\n\tquit - Exit the program.')
    elif userInput == '':
        print('Type \'help\' for commands.')