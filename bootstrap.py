# import core module
import subprocess
import os
from os import listdir
from os.path import isfile, join
import os.path
import shlex
import webbrowser
import zipfile
import time
from shutil import copyfile
import threading

# app meta data
_appVer = '0.03 beta'

# development to do list:
# - move google drive link to 'firefox setup' section to let user setup account while installing other apps
# - thread multitasking
# - useful apps download link

# pip module install func.
def install(package):
    subprocess.call(['pip', 'install', package])

# download func.
def download(_url, _filename):
    _fileuri = buildUri(_filename)
    wget.download(_url, out=_fileuri)
    _dFiles.append(_filename) # adds name of downloaded file to the list (for cleanup)
    print('') # wget ooutput line break

# run app
def run(_uri, _arg):
    _cmd = _arg.split(" ")
    _cmd.insert(0,_uri)
    subprocess.run(_cmd, bufsize=1, 
    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # redirect the output to null 
    #debug
    #subprocess.run(_cmd, bufsize=1)
def run2(_cmd):
    _arg = shlex.split(_cmd)
    subprocess.run(_arg, bufsize=1, 
    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # redirect the output to null
    #debug
    #subprocess.run(_arg, bufsize=1)

# file uri builder
def buildUri(_filename):
    _fileuri = os.path.join(_cd,_filename)
    # disabled because of bug
    #return _fileuri
    return _filename
def buildUri2(_filename):
    _fileuri = os.path.join(_cd,_filename)
    return _fileuri

# open url in browser
def openweb(_url):
    webbrowser.open(_url, new=2)

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

# get module
def getModule(_name):
    for i in range(3): # repeat until 3rd try
        try:
            install(_name)
        except:
            print("retrying...")
            pass # loop if not successful
        else:
            break # break loop if successful

# firefox install & configure thread
def instFirefox():
    # install firefox
    run(buildUri('firefox.exe'), '')

    # apply firefox pref
    run('taskkill', '/f /im firefox.exe /t')
    time.sleep(2)
    ff_topDir = os.path.join(_home,'AppData\Roaming\Mozilla\Firefox\Profiles')
    ff_profile = [f for f in listdir(ff_topDir) if not isfile(join(ff_topDir, f))] # only add directory to the candidate list
    ff_profdir = []

    for i in ff_profile: # leave only directory(ies) that has prefs.js
        if os.path.isfile(os.path.join(ff_topDir,i,'prefs.js')):
            ff_profdir.append(os.path.join(ff_topDir,i))

    for i in ff_profdir: # apply prefs.js to all directories
        try:
            copyfile(os.path.join(_cd,'prefs.js'), os.path.join(i,'prefs.js'))
            pass
        except Exception as e:
            print(e.message)
            pass
        else:
            print("Firefox installation & configuration complete.")
            print("Opening Google Drive...")
            openweb("https://drive.google.com/drive/folders/1myzqcvLCAUQzhABE-bE8rDc_yYhcmTo_?usp=sharing")
            pass

# cleanup
def cleanup():
    # delete downloaded files
    for i in _dFiles:
        try:
            os.remove(os.path.join(_cd,i))
        except:
            print('Error occured while deleting file \'' + i + '\'.')

# init
print('Welcome to Sajibang Configurator! (v.' + _appVer + ')\n\n')
print('======== Initialization ========')
print('Initializing...')
_cd = os.getcwd()
_home = os.getenv('USERPROFILE')
_dFiles = []
createDir(os.path.join(_home,"Desktop","work"))

# try importing wget
print('\nPreparing required modules...')
print('Downloading wget...')
getModule("wget")
import wget

# try importing winshell -> winshell pip problem. not creating shortcuts due to this
#getModule("pypiwin32")
#import pypiwin32
#
#getModule("winshell")
#import winshell

# disable windows update
print('\nDownloading Windows Update disable script...')
download("https://raw.githubusercontent.com/kimiroo/sjb/main/script/dwu.ps1", "dsu.ps1")
print('Disabling Windows update...')
run("sc.exe", "config wuauserv start=disabled")
run("sc.exe", "stop wuauserv")
run("powershell", "-noprofile -executionpolicy bypass -file " + os.path.join(_cd, "dsu.ps1"))

# kill adobe AdobeARM.exe
print('\nKilling Adobe services...')
run('taskkill', '/f /im AdobeARM.exe /t')
run("sc.exe", "config AdobeARMService start=disabled")
run("sc.exe", "stop AdobeARMService")

# download apps
print('\n======== Downloading Apps ========')
print("Downloading Firefox...")
download("https://download.mozilla.org/?product=firefox-stub&os=win&lang=ko", "firefox.exe")
download("https://raw.githubusercontent.com/kimiroo/sjb/main/data/prefs.js", "prefs.js") # download firefox pref
print("Installing Firefox now to save time...")
thInstFf = threading.Thread(instFirefox())
thInstFf.start()

print("\nDownloading VS Code...")
download("https://code.visualstudio.com/sha/download?build=stable&os=win32-x64", "vscode.exe")

print("\nDownloading PuTTY...")
download("https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe", "putty.exe")

print("\nDownloading FileZilla...")
download("https://download.filezilla-project.org/client/FileZilla_3.56.2_win64.zip", "filezilla.zip")

print("\nDownloading Git...")
download('https://github.com/git-for-windows/git/releases/download/v2.33.1.windows.1/Git-2.33.1-64-bit.exe', 'git.exe')

print("\nDownloading Bandizip...")
download('https://www.bandisoft.com/bandizip/dl.php?web', 'bandizip.exe')

print('\n======== Installing Apps ========')

print("Installing Bandizip...")
run(buildUri('bandizip.exe'), '/S')

print("Installing Git...")
run(buildUri('git.exe'), '/VERYSILENT /NORESTART')

print("Installing VS Code...")
run(buildUri('vscode.exe'), '/VERYSILENT /NORESTART /MERGETASKS=!runcode')

print("Copying PuTTY...")
copyfile(buildUri2('putty.exe'), os.path.join(_home,"Desktop","work","putty.exe"))

print("Extracting FileZilla...")
unzip('filezilla.zip', os.path.join(_home,"Desktop","work"))

# Code extension
# GitHub Pull Requests and Issues - github.vscode-pull-request-github
# Python - ms-python.python
# C/C++ - ms-vscode.cpptools

# Configure apps
print("\nConfiguring Apps...")
run2('cmd /c "C:\Program Files\Microsoft VS Code\\bin\code.cmd" --install-extension ms-python.python')
run2('cmd /c "C:\Program Files\Microsoft VS Code\\bin\code.cmd" --install-extension ms-vscode.cpptools')
run('cmd', '/c reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v HideFileExt /t REG_DWORD /d 0 /f') # show file extensions

# cleanup
print('\nCleaning up...')
cleanup()

print("\n======== Finished ========")

while True:
    print('Entering cmd...')
    run('cmd','')
