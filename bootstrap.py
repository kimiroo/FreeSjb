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

# pip module install func.
def install(package):
    subprocess.call(['pip', 'install', package])

# download func.
def download(_url, _filename):
    _fileuri = buildUri(_filename)
    wget.download(_url, out=_fileuri)

# run app
def run(_uri, _arg):
    _cmd = _uri + " " + _arg
    print(_cmd)
    subprocess.run(shlex.split(_cmd))

# file uri builder
def buildUri(_filename):
    _fileuri = os.path.join(_cd,_filename)
    # disabled because of bug
    #return _fileuri
    return _filename

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
# try importing wget
def getModule(_name):
    for i in range(3): # repeat until 3rd try
        try:
            install(_name)
        except:
            print("retrying...")
            pass # loop if not successful
        else:
            break # break loop if successful


# init
_cd = os.getcwd()
_home = os.getenv('USERPROFILE')
createDir(os.path.join(_home,"Desktop","work"))

# try importing wget
getModule("wget")
import wget

# try importing winshell -> winshell pip problem. not creating shortcuts due to this
#getModule("pypiwin32")
#import pypiwin32
#
#getModule("winshell")
#import winshell

# disable windows update
run("sc.exe", "config wuauserv start=disabled")
run("sc.exe", "stop wuauserv")
download("https://raw.githubusercontent.com/kimiroo/sjb/main/script/dwu.ps1", "dsu.ps1")
run("powershell", "-noprofile -executionpolicy bypass -file dwu.ps1")

# kill adobe AdobeARM.exe
subprocess.run('taskkill', '/f /im AdobeARM.exe /t')

# download apps
print("Downloading Firefox...")
download("https://download.mozilla.org/?product=firefox-stub&os=win&lang=ko", "firefox.exe")
print("Installing Firefox now to save time...")
run(buildUri('firefox.exe'), '')

# download firefox pref
download("https://raw.githubusercontent.com/kimiroo/sjb/main/data/prefs.js", "prefs.js")
# apply firefox pref
run('taskkill', '/f /im firefox.exe /t')
time.sleep(2)
ff_topDir = os.path.join(_home,'AppData\Roaming\Mozilla\Firefox\Profiles')
ff_profile = [f for f in listdir(ff_topDir) if not isfile(join(ff_topDir, f))]
ff_profdir = []

for i in ff_profile:
    if os.path.isfile(os.path.join(ff_topDir,i,'prefs.js')):
        ff_profdir.append(os.path.join(ff_topDir,i))

for i in ff_profdir:
    try:
        copyfile(os.path.join(_cd,'prefs.js'), os.path.join(i,'prefs.js'))
    except Exception as e:
        print(e.message)
        pass
    else:
        print("success")
        pass

print("\nDownloading VS Code...")
download("https://code.visualstudio.com/sha/download?build=stable&os=win32-x64", "vscode.exe")

print("\nDownloading PuTTY...")
download("https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe", "putty.exe")

print("\nDownloading FileZilla...")
download("https://dl2.cdn.filezilla-project.org/client/FileZilla_3.56.2_win64.zip?h=ojzFFbjfGn7WXTNB1lkeaQ&x=1636901311", "filezilla.zip")

print("\nDownloading Git...")
download('https://github.com/git-for-windows/git/releases/download/v2.33.1.windows.1/Git-2.33.1-64-bit.exe', 'git.exe')

print("\nDownloading Bandizip...")
download('https://www.bandisoft.com/bandizip/dl.php?web', 'bandizip.exe')

print("\n====Installing Apps====")

print("Installing Bandizip...")
run(buildUri('bandizip.exe'), '/S')

print("Installing Git...")
run(buildUri('git.exe'), '/VERYSILENT /NORESTART')

print("Installing VS Code...")
run(buildUri('vscode.exe'), '/VERYSILENT /NORESTART /MERGETASKS=!runcode')

print("Copying PuTTY...")
copyfile(buildUri('putty.exe'), os.path.join(_home,"Desktop","work"))

print("Extracting FileZilla...")
unzip('filezilla.zip', os.path.join(_home,"Desktop","work"))

# Code extension
# GitHub Pull Requests and Issues - github.vscode-pull-request-github
# Python - ms-python.python
# C/C++ - ms-vscode.cpptools

print("==== Configuring Apps ====")
subprocess.run('cmd', "code --install-extension ms-python.python")
subprocess.run(['cmd', 'code --install-extension ms-vscode.cpptools'])
subprocess.run(['powershell', 'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v HideFileExt /t REG_DWORD /d 0 /f'])

print("==== Finished ====")
print("Opening Google Drive...")
openweb("https://drive.google.com/drive/folders/1myzqcvLCAUQzhABE-bE8rDc_yYhcmTo_?usp=sharing")