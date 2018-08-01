from os import system
from time import sleep
from random import randint
from platform import system as osdetect
from colorama import init
init()
from colorama import Fore, Style, Back
if osdetect() == "Windows":
    system('color 1f'), sleep(0.05)
print(Fore.CYAN + Back.BLUE + Style.BRIGHT + "\n\n    RotoWare Scandisk"), sleep(0.01)
print("    ----------------------------------------------------------------------"), sleep(0.01)
if not "1" in open("safeshutdown.txt").read():
    print("\n    Because PythonOS was not properly shut down,"), sleep(0.01)
    print("    one or more of your disk drives may have errors on it."), sleep(0.01)
    print(Fore.WHITE + Style.NORMAL + "\n    To avoid seeing this message again, always shut down"), sleep(0.01)
    print("    your computer by typing \"exit\" or \"shutdown\""), sleep(0.01)
    print("    at the command line."), sleep(0.01)
    print("\n    Scandisk is now checking drive C for errors:"), sleep(0.01)
    print("\n\n\n\n\n\n\n")
else:
    print(Fore.WHITE + Style.NORMAL +"\n    Scandisk is now checking drive C for errors:"), sleep(0.01)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
print(Fore.CYAN + Style.BRIGHT +"    ----------------------------------------------------------------------"), sleep(0.5)
print("      " + "0" + "% complete" + Fore.YELLOW + "      ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒", end='\r'), sleep(1.5)
for x in range(1, 10):
    print(Fore.CYAN + "      " + str(x) + "% complete" + Fore.YELLOW + "      " + "█"*int(x/2) + "▒"*int((50)-(x/2)), end='\r'), sleep(0.08)
for x in range(10,100):
    print(Fore.CYAN + "      " + str(x) + "% complete" + Fore.YELLOW + "     " + "█"*int(x/2) + "▒"*int((50)-(x/2)), end='\r'), sleep(0.08)
print(Fore.CYAN + "      " + str(100) + "% complete" + Fore.YELLOW + "    " + "█"*50, end='\r'), sleep(0.08)
sleep(2)
if osdetect() == "Windows":
    system('cls')
else:
    system('clear')
error = randint(1,51)
print(Fore.CYAN + "\n\n    RotoWare Scandisk"), sleep(0.05)
print("    ----------------------------------------------------------------------"), sleep(0.01)
if error == 48:
    print(Fore.WHITE + Style.NORMAL + "\n    Drive C: scanned sucessfully. Some errors were found and repaired."), sleep(0.01)
else:
    print(Fore.WHITE + Style.NORMAL + "\n    Drive C: scanned sucessfully. No errors found."), sleep(0.01)
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n"), sleep(0.01)
print(Fore.CYAN + Style.BRIGHT + "    ----------------------------------------------------------------------"), sleep(2)
