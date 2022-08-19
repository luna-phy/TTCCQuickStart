import os, requests, subprocess, json

class ClashLauncher:
    localGamePath = os.getenv('LOCALAPPDATA') + '\\Corporate Clash\\'
    APIRegtPath = 'https://corporateclash.net/api/launcher/v1/register'
    APILognPath = 'https://corporateclash.net/api/launcher/v1/login'
    APIDistPath = 'https://corporateclash.net/api/v1/districts.js'
    APIMetaPath = 'https://corporateclash.net/api/v1/game_info.js'
    APIRevoPath = 'https://corporateclash.net/api/launcher/v1/revoke_self'
    gameServer = 'gs.corporateclash.net'
    configPath = os.path.dirname(__file__) + '\\config.json'

    activeDistricts = []

    # dictionaries to write to the config.json file
    accounts = {}       # stores all account usernames/tokens
    options = {}        # stores user-defined launch settings

    targetAccount = 0
    targetToonID = -1
    targetDistrict = ''

    def __init__(self):
        self.loadConfig()
        self.handleOptions()
        self.getDistricts()
        
        if not self.isGameOpen()[0]:
            print('Warning: Gameserver closed (%s).' % self.isGameOpen()[1])

    def loadConfig(self):
        try:
            file = json.load(open(self.configPath))

            self.accounts = file["accounts"]
            self.options = file["options"]
        except:
            with open(self.configPath, 'w') as file:
                json.dump({"accounts": {}, "options": {}}, file, indent = 4)
                print('Generated empty config.json file.')
            return

    def handleOptions(self):
        userPreferences = json.load(open(self.localGamePath + 'preferences.json'))
        if not self.options:
            return

        for option, value in self.options.items():
            userPreferences[option] = value

        with open(self.localGamePath + 'preferences.json', 'w') as file:
            json.dump(userPreferences, file, indent = 4)
        self.saveConfig()

    def saveConfig(self):
        with open(self.configPath, 'w') as file:
            json.dump({"accounts": self.accounts, "options": self.options}, file, indent = 4)

    def getDistricts(self):
        districts = requests.get(self.APIDistPath).json()
        if districts:
            for district in districts:
                if district['online']:
                    self.activeDistricts.append(district['name'])

        if not self.activeDistricts:
            print('Warning: No active districts detected?')

    def isGameOpen(self) -> tuple:
        response = requests.get(self.APIMetaPath).json()
        return (not response['production_closed'], response['production_closed_reason'])

    def register(self, username, password) -> bool:
        # if the current username trying to be registered exists in config.json, revoke that token, tell the server to revoke it, and replace it with a newly given token
        # if the user somehow has an expired token (like if they revoked it manually before using it), give a new token and replace it anyways
        if username in self.accounts.keys():
            revoke = requests.post(self.APIRevoPath, headers = {'Authorization': f'Bearer {self.accounts[username]}'}).json()
            if 'bad_token' in revoke:
                print(f'Revoking old token (expired) for username {username}.')
            elif 'status' in revoke:
                print(f"Revoked old token for username {username}.")

        response = requests.post(self.APIRegtPath, json = {'username': username, 'password': password, 'friendly': 'TTCCQuickstart'}).json()

        print(response['message'])
        if response['status']:
            self.accounts[username] = response['token']
            self.saveConfig()
        return response['status']

    def connect(self, accID, toonID, district) -> bool:
        # error handling
        if not self.accounts:
            print('No accounts. Have you registered an account with "--register"?')
            return False
        elif accID > len(self.accounts):
            print('Account ID %i exceeds list of registered accounts. Current amount of accounts: %i' % (accID, len(self.accounts) + 1))
            return False

        dispUN, token = list(self.accounts)[accID], list(self.accounts.values())[accID]

        print('Connecting with user "%s"...' % dispUN)
        response = requests.post(self.APILognPath, headers = {'Authorization': f'Bearer {token}'}).json()

        if 'bad_token' in response:
            print('Unauthorized token used. Try re-registering your account with --register.')
            return False

        print(response['message'])
        if response['status']:
            # handle district select
            targetDistrict = ''
            for dist in self.activeDistricts:
                if district == '':
                    break
                if district.lower() in dist.lower():
                    targetDistrict = dist
                    print('Using %s district.' % dist)
                    break
            
            if targetDistrict == '':
                print('Warning: Specified district does not exist, using random district.')

            # handle toon select
            if not (-1 < toonID < 6):
                print('Warning: Toon ID out of bounds, ignoring.')
            else:
                print('Using Toon ID %i.' % toonID)
            toonSlot = str(toonID) if (-1 < toonID < 6) else ''

            subprocess.run(self.localGamePath + 'CorporateClash.exe', cwd = self.localGamePath, env = dict(os.environ, TT_GAMESERVER = self.gameServer, TT_PLAYCOOKIE = response['token'], FORCE_TOON_SLOT = toonSlot, FORCE_DISTRICT = targetDistrict))
        return response['status']

l = ClashLauncher()
l.handleOptions()