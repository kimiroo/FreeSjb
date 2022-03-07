# import core module
import os, subprocess, shlex, zipfile, time, threading, wget

# app meta data
_appVer = 'v0.06 beta (quick)'

def init():
    global _cd, _home, _dFiles, _tmp
    _cd = os.getcwd()
    _home = os.getenv('USERPROFILE')
    _dFiles = []
    _tmp = os.path.join(_home,".temp")
    cleanup
    createDir(_tmp)

# download func.
def download(_url, _filename):
    _fileuri = buildUri(_filename)
    wget.download(_url, out=_fileuri, bar=wget_bar)
    _dFiles.append(_filename) # adds name of downloaded file to the list (for cleanup)
    print('Downloading ' + os.path.basename(_filename) + ' complete.') # wget ooutput line break

def wget_bar(current, total, width=80):
    pass

# run app
def run(_uri, _arg):
    _cmd = _arg.split(" ")
    _cmd.insert(0,_uri)
    #subprocess.run(_cmd, bufsize=1, 
    #stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # redirect the output to null 
    #debug
    subprocess.run(_cmd, bufsize=1)
def run2(_cmd):
    _arg = shlex.split(_cmd)
    #subprocess.run(_arg, bufsize=1, 
    #stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # redirect the output to null
    #debug
    subprocess.run(_arg, bufsize=1)
def run_silent(_uri, _arg):
    _cmd = _arg.split(" ")
    _cmd.insert(0,_uri)
    #subprocess.run(_cmd, bufsize=1, 
    #stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # redirect the output to null 
    #debug
    subprocess.run(_cmd, bufsize=1, 
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT)
def run2_silent(_cmd):
    _arg = shlex.split(_cmd)
    #subprocess.run(_arg, bufsize=1, 
    #stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # redirect the output to null
    #debug
    subprocess.run(_arg, bufsize=1, 
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT)

# file uri builder
def buildUri(_filename):
    _fileuri = os.path.join(_cd,_filename)
    return _fileuri

# unzip
def unzip(_zipfile, _target):
    _zipf = zipfile.ZipFile(_zipfile)
    _zipf.extractall(_target)
    _zipf.close

# create dir
def createDir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

# cleanup
def cleanup():
    pass

def downThread(_urlList, _appList):
    global finDownList
    finDownList = []
    if len(_urlList) != len(_appList):
        raise ListLengthUnmatch('List of given lists does not match.')
    else:
        for i in range(len(_urlList)):
            for loop in range(3):
                trial = 0
                try:
                    download(_urlList[i], os.path.join(_tmp, _appList[i]+".exe"))
                except Exception as e:
                    print(e)
                    print("Retrying...")
                    trial = 1
                else:
                    trial = 0
                    break
            if trial == 0:
                finDownList.append(_appList[i-1])
            else:
                raise Exception('Downloading',_appList[i-1],'has failed.')

def setupThread(_appList, _argumentList):
    currentStage = 0
    while currentStage != len(_appList):
        if len(finDownList) > currentStage:
            print('Installing ' + _appList[currentStage] + '...')
            for loop in range(3):
                fail = False
                try:
                    run(os.path.join(_tmp, _appList[currentStage]+".exe"), _argumentList[currentStage])
                except Exception as e:
                    print(e)
                    print('Retrying...')
                    fail = True
                else:
                    currentStage += 1
                    fail = False
                    break
            if fail == True:
                raise Exception('Installing',_appList[i-1],'has failed.')
            else:
                pass
        time.sleep(1)

def disableUpdate(loop=False):
    # download windows update disable script

    if os.path.isfile(os.path.join(_tmp, "dsu.ps1")) == False:
        print('Downloading script...')
        download("https://raw.githubusercontent.com/kimiroo/FreeSjb/main/script/dwu.ps1", os.path.join(_tmp, "dsu.ps1"))
        _winScript = True

    if loop:
        while True:
            updateDisabler()
            print('10 Seconds cool time')
            time.sleep(10)
            print('')
    else:
        updateDisabler()

def updateDisabler():
        # disable windows update
        print('Disabling Windows update...')
        run_silent("sc.exe", "config wuauserv start=disabled")
        run_silent("sc.exe", "stop wuauserv")
        run_silent("powershell", "-noprofile -executionpolicy bypass -file " + os.path.join(_tmp, "dsu.ps1"))
        # kill adobe AdobeARM.exe
        print('Disabling Adobe services...')
        run_silent('taskkill', '/f /im AdobeARM.exe /t')
        run_silent("sc.exe", "config AdobeARMService start=disabled")
        run_silent("sc.exe", "stop AdobeARMService")

def main():
    # init
    print('Welcome to Sajibang QUICK Configurator! (v.' + _appVer + ')\n\n')

    print('Initializing...')
    init()

    print('\nDisabling Update Services...')
    _winScript = False
    disableUpdate()

    print('\nInstalling Applications:')
    _urlList = [
        'https://dl.google.com/tag/s/appguid={8A69D345-D564-463C-AFF1-A69D9E530F96}&iid={2E6DB249-C5AA-5A11-4DB4-BDE2BAD5630C}&lang=ko&browser=4&usagestats=0&appname=Google%20Chrome&needsadmin=prefers&ap=x64-stable-statsdef_1&installdataindex=empty/update2/installers/ChromeSetup.exe',
        'https://www.bandisoft.com/bandizip/dl.php?std-all'
        # PyShell
    ]
    _appList = [
        'chrome',
        'bandizip'
        # PyShell
    ]
    _argumentList = [
        '/silent /install',
        '/S'
        # PyShell
    ]

    t_down = threading.Thread(target=downThread, args=(_urlList, _appList))
    t_down.daemon = True 
    t_down.start()
    t_setup = threading.Thread(target=setupThread, args=(_appList, _argumentList))
    t_setup.daemon = True
    t_setup.start()

    t_setup.join()
    print(str(finDownList))

    print('\nDownloading PyShell...')
    download('https://github.com/kimiroo/PyShell/releases/latest/download/PyShell.zip', os.path.join(_tmp, "PyShell.zip"))
    print('Installing PyShell...')
    createDir(os.path.join(_home, "pysh"))
    unzip(os.path.join(_tmp, "PyShell.zip"), os.path.join(_home, "pysh"))
    launchParameter_PySh = '/c ' + os.path.join(_home, "pysh","install.bat")
    run(os.path.join(_home, "pysh","pysh.exe"), launchParameter_PySh)

    print('\nConfiguring Applications...')
    download('https://raw.githubusercontent.com/kimiroo/FreeSjb/main/data/bandizip_conf.reg', os.path.join(_tmp, "bandizip_conf.reg"))
    launchParameter_bdz = '/c reg import ' + os.path.join(_tmp, "bandizip_conf.reg")
    run(os.path.join(_home, "pysh","pysh.exe"), launchParameter_bdz)

    print('\nDone.')
    print('\nEvery Installation & Configuration Process has been completed successfully.')

    print('\n\nStarting Anti Update MicroServices...')
    print('Note: This will loop infinitely untill this console window is closed.\n      Minimize or put this window on other workspace to hide this process.')
    t_disable = threading.Thread(target=disableUpdate, args=(True,))
    t_disable.daemon = True
    t_disable.start()
    t_disable.join()

if __name__ == '__main__':
    main()
