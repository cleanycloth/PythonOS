##System File Checker

##Can be used in the OS (to make sure files weren't moved during operation) or
##externally to make sure everything is where it should be.

from time import sleep
from os import path, system, remove
from platform import system as osdetect
try:
    from colorama import init
    init()
    from colorama import Fore, Style, Back
except:
    print("Colorama is missing! Cannot continue. Please reinstall colorama.")
    sleep(5)
    exit()
def clear():
    if osdetect() == "Windows":
        system('cls')
    else:
        system('clear')
def writefiles(filename, data):
    file = open(filename, "w")
    file.write(data), file.close()
filelist = (['bios.py',
             'checkfiles.py',
             'cortana.py',
             'loadanimation.py',
             'login.py',
             'logos.py',
             'PythonOS.py',
             'runtests.py',
             'scandisk.py',
             'start.py',
             'vlc.py',
             'convert.py',
             'Documents/m8b5.py',
             'Documents/k.exe',
             'Documents/textadv/textadv2.py',
             'Documents/unit1test.py',
             'Sounds/logoff.wav',
             'Sounds/logon.wav',
             'Sounds/shut.wav',
             'Sounds/start.wav',
             'Sounds/uac.wav'])
x = 0
clear()
print("Checking for PythonOS system files, please wait.")
while x < len(filelist):
    print(Fore.WHITE + Style.NORMAL + filelist[x] + ".",end='\r'), sleep(0.15)
    print(Fore.WHITE + Style.NORMAL + filelist[x] + "..",end='\r'), sleep(0.15)
    print(Fore.WHITE + Style.NORMAL + filelist[x] + "...",end='\r'), sleep(0.15)
    if path.exists(filelist[x]):
        print(filelist[x] + "..." + Fore.GREEN + Style.BRIGHT + "ok!")
    else:
        print(filelist[x] + "..." + Fore.RED + Style.BRIGHT + "error!")
    x += 1
    sleep(0.1)
print(Fore.WHITE + Style.NORMAL + "Waiting 5 seconds...")
sleep(5)
print("Starting Scandisk (if present)...")
sleep(2)
clear()
try:
    writefiles('safeshutdown.txt',"1")
    import scandisk
    clear()
    system('color 07')
    writefiles('safeshutdown.txt',"0")
except ImportError:
    print("Failed to run Scandisk.")
    sleep(1)
    remove("safeshutdown.txt")
#print(Fore.WHITE + Style.NORMAL + "Log saved to Documents/testlog.log")
#sleep(3)
