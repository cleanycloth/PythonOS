from random import randint
from os import system
from time import sleep
rand = randint(1,50)
def crash():
    system('color 1f')
    if rand == 27:
        print("*** STOP: 0x0000007F (0xC107C534, 0x00000000, 0x804F5830, 0x00000000)"),     sleep(0.01)
        print("UNEXPECTED_KERNEL_MODE_TRAP"),                                               sleep(0.01)
    else:
        print("*** STOP: 0xDEADDEAD (0xC107C534, 0x00000000, 0x804F5830, 0x00000000)"),     sleep(0.01)
        print("MANUALLY_INITIATED_CRASH1"),                                                 sleep(0.01)
    print("\n*** Address 804F5380 base at 80400000, Datestamp 45ec3c8f - ntoskrnl.exe"),    sleep(0.01)
    print("\nIf this is the first time you've seen this stop error screen,"),               sleep(0.01)
    print("restart your computer. If this screen appears again, follow"),                   sleep(0.01)
    print("these steps:"),                                                                  sleep(0.01)
    print("\nCheck to make sure any new hardware or software is properly installed."),      sleep(0.01)
    print("If this is a new installation, ask your hardware or software manufacturer"),     sleep(0.01)
    print("for any PythonOS updates you might need."),                                      sleep(0.01)
    print("\nIf problems continue, disable or remove any newly installed hardware"),        sleep(0.01)
    print("or software. Disable BIOS memory options such as caching or shadowing."),        sleep(0.01)
    print("If you need to use Safe Mode to remove or disable components, restart"),         sleep(0.01)
    print("your computer, press F8 to select Advanced Startup Options, and then"),          sleep(0.01)
    print("select safemode."),                                                              sleep(0.01)
    print("\nRefer to your Getting Started manual for more information on"),                sleep(0.01)
    print("troubleshooting Stop errors.\n"),                                                sleep(0.01)
    sleep(1)
    for x in range(1,101):
        print("Preparing dump of physical memory... (" + str(x) + "%)", end='\r'),          sleep(0.05)
    print("\nPhysical memory dump complete."),                                              sleep(0.5)
    print("Contact your system administrator for more information on this STOP error."),    sleep(4)
    print("Attempting to restart PythonOS."),                                               sleep(1)
    exit()

crash()
