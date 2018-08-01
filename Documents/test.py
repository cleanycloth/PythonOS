import _thread
from os import system
from time import sleep
def playsound():
    system('C:\\PROGRA~2\\videolan\\vlc\\vlc.exe --intf dummy --dummy-quiet --play-and-exit loop.s3m')

def testmessage():
    for x in range(1,51):
        print("Counting: " , x, end='\r')
        sleep(0.1)

_thread.start_new_thread( playsound, () )
testmessage()
