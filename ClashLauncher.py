import os, requests, subprocess

class ClashLauncher:
    gamePath = os.getenv('LOCALAPPDATA') + '\\Corporate Clash\\'
    gameAPIPath = 'https://corporateclash.net/api/v1/login/'

    accounts = {
        '1':  ['', ''],
        '2':  ['', ''],
        '3':  ['', ''],
        '4':  ['', '']
    }

    districts = {
        'anvil'     :   'Anvil Acres',
        'cupcake'   :   'Cupcake Cove',
        'quicksand' :   'Quicksand Quarry',
        'tesla'     :   'Tesla Tundra',
        'highdive'  :   'High-Dive Hills',
        'hypno'     :   'Hypno Heights',
        'seltzer'   :   'Seltzer Summit',
        'kazoo'     :   'Kazoo Kanyon'
    }

    targetAccount = 1
    targetToonID = 1
    targetDistrict = ''

    def __init__(self, accID = '1', toonID = '-1', district = ''):
        if accID not in self.accounts:
            raise IndexError('Account ID out of bounds')
        if int(toonID) < -1 or int(toonID) > 5:
            raise IndexError('Toon ID must be between -1 and 5, inclusive')
        if district not in self.districts:
            print('\'{}\' is not a valid district, choosing random district'.format(district))
            self.targetDistrict = ''

        self.targetAccount = accID
        
        if toonID == '-1':
            self.targetToonID = ''
        else:
            self.targetToonID = toonID

    def connect(self) -> bool:
        username = self.accounts.get(self.targetAccount)[0]
        password = self.accounts.get(self.targetAccount)[1]
        response = requests.post(self.gameAPIPath + username, data = {'password': password}, headers = {'x-realm': 'production'}).json()

        if response['status']:
            gameserver = 'gs.corporateclash.net'
            cookie = response['token']

            print('Login success. Server gave token {} ({})'.format(cookie, response['friendlyreason']))

            subprocess.run(self.gamePath + 'CorporateClash.exe', cwd = self.gamePath, env = dict(os.environ, TT_GAMESERVER = gameserver, TT_PLAYCOOKIE = cookie, FORCE_TOON_SLOT = str(self.targetToonID), FORCE_DISTRICT = str(self.targetDistrict)))
            return True
        else:
            print('Login failed. Server gave server code {} ({})'.format(response['reason'], response['friendlyreason']))
            return False
