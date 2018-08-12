from time import sleep
from os import system, path, remove
from platform import system as osdetect
error = 0
filelist = (['Documents/k.exe',
            'Documents/m8b5.py',
            'Documents/khelp.hlp',
            'Documents/nhelp.hlp',
            'Documents/pythonoshelp.hlp',
            'commands.lst'
            'scandisk.py',
            'login.py',
            'loadanimation.py',
            'cortana.py',
            'Documents/textadv/textadv2.py',
            'vlc.py',
            'colorama',
            'logos.py',
            'runtests.py',
            'convert.py',
            'Sounds/logoff.wav',
            'Sounds/logon.wav',
            'Sounds/shut.wav',
            'Sounds/start.wav',
            'Sounds/uac.wav'])
def screenclear():
    if osdetect() == "Windows":
        system('cls')
    else:
        system('clear')
for x in range(len(filelist)):
    if not path.exists(filelist[x]):
        error = 1
        break
if error == 1:
    sleep(1)
    screenclear()
    print("PythonOS cannot continue loading because the following files are missing:")
    for x in range(len(filelist)):
        if not path.exists(filelist[x]):
            print("/" + filelist[x])
    print("Replace these files, and press enter to restart.")
    file = open('shutdown.txt', "w")
    file.write("1"), file.close() 
    input("")
    remove('lock')


