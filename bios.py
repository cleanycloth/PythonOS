from time import sleep
from random import randint
from platform import system as osdetect
if osdetect() == "Windows":
    from winsound import Beep as beep
else:
    def beep(thinga, thingb):
     print("", end='\r')
rd = randint(1,100)
print("PhoenixBIOS 4.0 Release 6.0"), sleep(0.05)
print("Copyright 1985-2001 Phoenix Technologies Ltd."), sleep(0.05)
print("All Rights Reserved"), sleep(0.05)
print("Copyright 2016 RotoWare"), sleep(0.05)
print("PythonBIOS build 034\n"), sleep(0.5)
print("640K System RAM Passed"), sleep(1)
if not rd == 57:
    for a in range(0,129):
        print(str(a+a+a+a) + "M Extended RAM Passed", end='\r'), sleep(0.001)
else:
    for a in range(0,257):
        print(str(a+a) + "M Extended RAM Passed", end='\r'), sleep(0.001)
    sleep(2)
    for a in range(0,513):
        print(str(a) + "M Extended RAM Passed", end='\r'), sleep(0.001)
print(""), sleep(1)
print("Scanning IDE/SATA channels for devices...", end='\r'), sleep(2)
print("Fixed Disk 0: RotoWare SATA Virtual Hard Drive"), sleep(0.1)
print("ATAPI CD-ROM: RotoWare SATA Virtual DVD-RW Drive"), sleep(0.1)
print("Keyboard initialized")
print("Mouse initialized")
if not rd == 57:
    print("\nLoading modules...", end='\r'), sleep(1)
    print("Loading modules completed successfully.")
    print("\n\n\n\n\n\n\n")
else:
    print("\nLoading modules...", end='\r'), sleep(1)
    print("Loading modules completed successfully.")
    sleep(1)
    beep(800,500)
    beep(800,500)
    print("\nCMOS checksum error. Defaults loaded.")
    sleep(2)
    print("\n\n\n\n\n")
print("Press F2 to enter SETUP, F12 for Network Boot, ESC for Boot menu"), sleep(1.5)
beep(800,500)
