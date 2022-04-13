import os, json, requests, hashlib, gzip, bz2

class ClashResourceFile:
    fileName = ''
    filePath = ''
    sha1 = ''
    compressedSha1 = ''

    def __init__(self, fn, fp, s1, cs1):
        self.fileName = fn
        self.filePath = fp
        self.sha1 = s1
        self.compressedSha1 = cs1

class ClashPatcher:
    patchManifest = list()
    filesNeeded = list()

    manifestTargetBase = 'https://corporateclash.net/api/v1/launcher/manifest/v2/windows_production.js'
    manifestTargetRes = 'https://corporateclash.net/api/v1/launcher/manifest/v2/resources_production.js'
    manifestUpdateUrl = 'https://aws1.corporateclash.net/productionv2/'

    gameDirectory = os.getenv('LOCALAPPDATA') + '\\Corporate Clash\\'

    def __init__(self):
        pass

    def getPatchManifest(self): 
        manifestJson = requests.get(self.manifestTargetBase)
        if manifestJson.status_code != 200:
            raise ConnectionError(manifestJson.status_code)

        manifest = json.loads(manifestJson.text)
        for file in manifest['files']:
            self.patchManifest.append(ClashResourceFile(file['fileName'], file['filePath'], file['sha1'], file['compressed_sha1']))

        manifestJson = requests.get(self.manifestTargetRes)
        if manifestJson.status_code != 200:
            raise ConnectionError(manifestJson.status_code)

        manifest = json.loads(manifestJson.text)
        for file in manifest['files']:
            self.patchManifest.append(ClashResourceFile(file['fileName'], file['filePath'], file['sha1'], file['compressed_sha1']))

    def checkLocalFiles(self, displayOutput: bool = False):
        for file in self.patchManifest:
            fullPath = self.gameDirectory + file.filePath

            if os.path.exists(fullPath):
                fileHash = self.sha1HashFile(fullPath)
                    
                if fileHash == file.sha1:
                    continue
            
            if displayOutput:
                print('File \'' +  file.fileName + '\' at \'root/' + file.filePath + '\' needs updating. Queuing.')
            self.filesNeeded.append(file)

    def isGameUpdated(self) -> bool:
        self.getPatchManifest()
        self.checkLocalFiles(False)

        value = not self.filesNeeded

        self.patchManifest.clear()
        self.filesNeeded.clear()

        return value

    def sha1HashFile(self, filePath) -> str:
        if os.path.exists(filePath):
            with open(filePath, 'rb') as f:
                fileHash = hashlib.sha1()
                while chunk := f.read(8192):
                    fileHash.update(chunk)

            return fileHash.hexdigest()
        else:
            raise FileNotFoundError

    def sha1HashString(self, s) -> str:
        bStr = bytes(s, encoding = 'UTF-8')
        hash = hashlib.sha1(bStr)
        return hash.hexdigest()

    def verifyFile(self, path: str, hash: str) -> bool:
        return self.sha1HashFile(path) == hash

    def decompressFile(self, bz2file: str, localFile: str, action: str):
        with open(bz2file, 'rb') as b:
            with open(localFile, 'wb') as l:
                if action == 'bzip2':
                    l.write(bz2.decompress(b.read()))
                elif action == 'gzip':
                    l.write(gzip.decompress(b.read()))
        return

    def extractFile(self, dlPath: str, exPath: str, action: str) -> int:
        try:
            self.decompressFile(dlPath, exPath, action)
            return 0
        except:
            os.remove(exPath)
            return -1
        finally:
            os.remove(dlPath)

    def downloadFile(self, url: str, filepath: str) -> int:
        try:
            response = requests.get(url)
            stream = response.content

            with open(filepath, 'wb') as f:
                f.write(stream)
            
            return 0
        except:
            return -1

    def acquireFile(self, file: ClashResourceFile):
        fileTarget = self.sha1HashString(file.filePath)

        url = self.manifestUpdateUrl + fileTarget
        downloadPath = self.gameDirectory + fileTarget
        extractedPath = downloadPath + '~'

        state = self.downloadFile(url, downloadPath)

        if state != 0:
            os.remove(downloadPath)
            raise OSError
        
        if not self.verifyFile(downloadPath, file.compressedSha1):
            raise OSError

        if self.extractFile(downloadPath, extractedPath, 'gzip') != 0:
            raise OSError

        if self.verifyFile(extractedPath, file.sha1):
            file.fileName = fileTarget + '~'
            return
        else:
            raise OSError
    
    def downloadGameFiles(self):
        for file in self.filesNeeded:
            self.acquireFile(file)

    def patchGameFiles(self):
        for file in self.filesNeeded:
            localPath = self.gameDirectory + file.filePath
            localDir = os.path.dirname(localPath)

            if os.path.isdir(localDir):
                if os.path.isfile(localPath):
                    os.remove(localPath)
            else:
                os.mkdir(localDir)

            os.replace(self.gameDirectory + file.fileName, self.gameDirectory + file.filePath)        

    def run(self):
        print('Fetching new patch manifest')
        self.getPatchManifest()
        print('Checking local files for inconsistencies')
        self.checkLocalFiles(True)
        print('Downloading updated gamefiles')
        self.downloadGameFiles()
        print('Patching local gamefiles')
        self.patchGameFiles()