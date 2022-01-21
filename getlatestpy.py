from bs4 import BeautifulSoup
import urllib.request
from functools import cmp_to_key

def compVer(inp1, inp2):
    arr1 = inp1.split('.')
    arr2 = inp2.split('.')

    arr1 = [int(i) for i in arr1]
    arr2 = [int(i) for i in arr2]

    if arr1[0] > arr2[0]:
        return -1
    elif arr1[0] < arr2[0]:
        return 1
    else:
        if arr1[1] > arr2[1]:
            return -1
        elif arr1[1] < arr2[1]:
            return 1
        else:
            if arr1[2] > arr2[2]:
                return -1
            elif arr1[2] < arr2[2]:
                return 1
            else:
                return 0

def getLatestPythonVer():
    web = urllib.request.urlopen('https://www.python.org/downloads/')
    soup = BeautifulSoup(web, 'html.parser')
    versionList = []

    for i in soup.select('span.release-number'):
        text = str(i.text).replace('Python ','')

        if text != 'Release version':
            versionList.append(text)

    versionList = sorted(versionList, key=cmp_to_key(compVer))

    return versionList[0]

def main():
    print(getLatestPythonVer())
    
if __name__ == '__main__':
    main()
