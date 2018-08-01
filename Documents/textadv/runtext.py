from os import system

while 1:
    system('cls')
    try:
        system("py.exe textadv2.py")
    except KeyboardInterrupt:
        print("Keyboard interrupt detected.")
    #vlc.MediaPlayer("chord.wav").play()
    res = input("\nRestart? ")
    if res == "n":
        exit()
