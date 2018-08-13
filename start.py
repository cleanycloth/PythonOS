from os import system, path, remove
from platform import system as osdetect
from time import sleep
global go
if osdetect() == "Windows":
	system('title PythonOS Launcher - Starting PythonOS...')
	system('mode con: cols=80 lines=25')
def checkfile():
    if not path.exists("shutdown.txt"):
        file = open('shutdown.txt', "w")
        file.close()

def launch():
    if osdetect() == "Windows":
        go = system('py.exe "PythonOS.py"')
    else:
        go = system('python3 "PythonOS.py"')
    if go == 1:
        print("\n\nAn error has occurred in PythonOS. Press enter to restart.")
        input("")
    checkfile()
    if not path.exists("PythonOS.py") and not path.exists("cmd.exe"):
        print("\n\nPythonOS executable is missing. Please reinstall PythonOS.")
        print("\n\nPress any key to restart.")
        input()
        remove("lock")
        go = 0
    if go == 2:
        print("\n\nUnable to start the virtual machine. Are you trying to run\nthe VM from a network location?\n\nPress enter to exit.")
        input("")
        remove("lock")
        exit()

while 1:
        if not path.exists("lock"):
            file = open('lock', "w")
            file.close()
        else:
            stop = input("WARNING!\nPythonOS seems to be already running or has recently crashed.\nStarting more than one instance of PythonOS is seriously not recommended!\n\nDo you wish to continue, and override this? [y/N]: ")
            if not stop.upper() == "Y":
                exit()
        try:
            launch()
        except(KeyboardInterrupt):
            print("\nForced system reset detected. PythonOS is now restarting.")
            remove("lock")
            sleep(3)
        if "1" in open("shutdown.txt").read():
            exit()
