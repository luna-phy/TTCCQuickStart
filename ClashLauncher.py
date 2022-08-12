import os, requests, subprocess, json

class ClashLauncher:
    localGamePath = os.getenv('LOCALAPPDATA') + '\\Corporate Clash\\'
    APIRegtPath = 'https://corporateclash.net/api/launcher/v1/register'
    APILognPath = 'https://corporateclash.net/api/launcher/v1/login'
    APIDistPath = 'https://corporateclash.net/api/v1/districts.js'
    APIMetaPath = 'https://corporateclash.net/api/v1/game_info.js'
    gameServer = 'gs.corporateclash.net'
    configPath = os.path.dirname(__file__) + '\\config.json'

    activeDistricts = []
    accounts = []

    targetAccount = 0
    targetToonID = -1
    targetDistrict = ''

    def __init__(self):
        self.loadConfig()
        self.getDistricts()
        
        if not self.isGameOpen():
            print('Warning: Gameserver closed.')

    def loadConfig(self):
        if not os.path.exists(self.configPath):
            with open(self.configPath, 'w') as file:
                json.dump({}, file, indent = 4)
            return
        else:
            file = json.load(open(self.configPath))
        
        for acc in file:
            self.accounts.append(acc)

    def saveConfig(self):
        with open(self.configPath, 'w') as file:
            json.dump(self.accounts, file, indent = 4)

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
        return (response['production_closed'], response['production_closed_reason'])

    def register(self, username, password) -> bool:
        if username in (elem for sublist in self.accounts for elem in sublist):
            print('That account is already registered. If the token is invalid, delete it from the configuration.')
            return False

        response = requests.post(self.APIRegtPath, json = {'username': username, 'password': password, 'friendly': 'TTCCQuickstart'}).json()

        print(response['message'])
        if response['status']:
            self.accounts.append((username, response['token']))
            self.saveConfig()
        return response['status']

    def connect(self, accID, toonID, district) -> bool:
        if not self.accounts:
            print('No accounts. Have you registered an account with "--register"?')
            return False

        dispUN, token = self.accounts[accID]

        print('Connecting with user "%s"...' % dispUN)
        response = requests.post(self.APILognPath, headers = {'Authorization': f'Bearer {token}'}).json()
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
                print('Specified district does not exist, using random district.')

            subprocess.run(self.localGamePath + 'CorporateClash.exe', cwd = self.localGamePath, env = dict(os.environ, TT_GAMESERVER = self.gameServer, TT_PLAYCOOKIE = response['token'], FORCE_TOON_SLOT = str(toonID) if (-1 < toonID < 6) else '', FORCE_DISTRICT = targetDistrict))
        return response['status']