import os, requests, subprocess, json

class ClashLauncher:
    gamePath = os.getenv('LOCALAPPDATA') + '\\Corporate Clash\\'
    gameAPIPath = 'https://corporateclash.net/api/v1/login/'
    gameserver = 'gs.corporateclash.net'
    accountsJsonPath = os.path.dirname(__file__) + '\\accounts.json'

    defaultJson = {'accounts': [{'username': 'username', 'password': 'password'}, {'username': 'username2', 'password': 'password2'}], 'params': {'realm': 'production', 'districts': ['Anvil Acres', 'Cupcake Cove', 'Quicksand Quarry', 'Tesla Tundra', 'High-Dive Hills', 'Hypno Heights', 'Seltzer Summit', 'Kazoo Kanyon']}}

    targetAccount = ''
    targetToonID = 1
    targetDistrict = ''
    targetRealm = ''

    def __init__(self, accID = 0, toonID = -1, district = ''):
        if not os.path.exists(self.accountsJsonPath):
            with open(self.accountsJsonPath, 'w') as file:
                json.dump(self.defaultJson, file, indent = 4)
            raise FileNotFoundError('%s does not exist. Generating default.' % self.accountsJsonPath)
        else:
            file = json.load(open(self.accountsJsonPath))

        if 'accounts' in file:
            if accID < 0:
                accID = 0
            if accID > len(file['accounts']):
                accID = len(file['accounts']) - 1

            if 'username' and 'password' in file['accounts'][accID]:
                self.targetAccount = file['accounts'][accID]
            else:
                raise KeyError('Username and/or password field do not exist!')
        else:
            raise KeyError('No accounts found?')

        if 'params' in file:
            if 'realm' in file['params']:
                self.targetRealm = file['params']['realm']
            else:
                self.targetRealm = 'production'
            
            if 'districts' not in file['params']:
                raise KeyError('No districts found!')
        else:
            raise KeyError('No parameters found?')

        for dst in file['params']['districts']:
            if district == '':
                break
            
            if district.lower() in dst.lower():
                self.targetDistrict = dst
                print('Using %s district.' % dst)
                break
        
        if self.targetDistrict == '':
            print('Specified district does not exist, using random district.')

        self.targetToonID = str(toonID) if (-1 < toonID < 6) else ''

    def overrideRealm(self, realm: str = 'production'):
        self.targetRealm = realm if realm == 'qa' else 'production'

    def connect(self) -> bool:
        username = self.targetAccount['username']
        password = self.targetAccount['password']
        response = requests.post(self.gameAPIPath + username, data = {'password': password}, headers = {'x-realm': self.targetRealm}).json()

        if response['status']:
            cookie = response['token']

            print('Login success. Server gave token {} ({})'.format(cookie, response['friendlyreason']))

            subprocess.run(self.gamePath + 'CorporateClash.exe', cwd = self.gamePath, env = dict(os.environ, TT_GAMESERVER = self.gameserver, TT_PLAYCOOKIE = cookie, FORCE_TOON_SLOT = self.targetToonID, FORCE_DISTRICT = str(self.targetDistrict)))
            return True
        else:
            print('Login failed. Server gave server code {} ({})'.format(response['reason'], response['friendlyreason']))
            return False
