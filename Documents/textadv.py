from time import sleep
from random import randint, choice
from winsound import Beep as beep
from os import system
#import vlc
#Credits:
#Launch song by Skaven
#Plot idea from Ubisoft
#Code by meeeeeeeeeeeeeeeeee

def splash():
    system('cls')
    print("""
   __  __      __  _ __  __         __
  / / / /___  / /_(_) /_/ /__  ____/ /
 / / / / __ \/ __/ / __/ / _ \/ __  / 
/ /_/ / / / / /_/ / /_/ /  __/ /_/ /  
\_______ /_/\__/_/___/_/\___/\__,_/   
 /_  __/__  _  __/ /_                 
  / / / _ \| |/_/ __/                 
 / / /  __/>  </ /_                   
/_/__\\\\\\\/_/|_|\__/                   
  / ____/___ _____ ___  ___           
 / / __/ __ `/ __ `__ \/ _ \          
/ /_/ / /_/ / / / / / /  __/          
\____/\__,_/_/ /_/ /_/\___/           
                                      """)                                           
    #vlc.MediaPlayer("loop.s3m").play()

def incorrectgen():
    incorrectanswer = choice([
        "That's not in the list.",
        "No, you idiot. Read the list again.",
        "*sigh*, can you not read?",
        "Try again.",
        "Wrong.",
        "This isn't part of the script...",
        "Why? Are you deliberately trying to be annoying?",
        "Can't do that.",
        "No.",
        "I'm sure you'll get it right the next time."])
    return incorrectanswer

def leave():
    sure = input("Are you sure you want to quit? ;-; ")
    if sure.lower() == "y":
        print("Quitting to prompt.")
        exit()

def start():
    print("Welcome to \"Untitled Text Game\".")
    name = input("To start, please enter your name. : ")
    print("Excellent, thank you, " + name + ".")
    print("Alright, let's start this journey!")
    sleep(1)

def premise():
    print("\nThe premise:\n")
    print("""Life was great. You had just finished your college degree, you
were well off, your parents were extremely happy, and you had an SO to call
yours. Except, that all suddenly changed when you went on holiday to Bangkok,
where you have to survive to find your captured SO.

This is where the story begins.""")

def room1():
    roadtodeath = 3
    print("""\n\nYou awaken in a cage. A man is going through your phone, looking
at all your photos and videos, while talking to you. You try and go for him,
but you realise you are tied to the outer cage. There is another person in
the cage with you.

You can:
1. Ask for help (they might have an idea on what to do)
2. Sit there and wait for something else to happen.
3. Try and untie yourself.""")
    while 1:
        room1do = input("\nWhat do you wish to do? : ")
        if room1do == "1":
            room1sub1()
        elif room1do == "2":
            print("Nothing really happens.")
            roadtodeath = roadtodeath - 1
            if roadtodeath == 0:
                #vlc.MediaPlayer("over.wav").play()
                print("You waited so long that you dehydrated and died.\n\nGAME OVER.")
                sleep(4.5)
                exit()
        elif room1do == "3":
            print("You try to untie yourself, but it doesn't work. There isn't enough slack in the rope.")
        elif room1do == "q":
            leave()
        else:
            print(incorrectgen())

def room1sub1():
    bored = 2
    print("-"*79)
    print("You whisper to the other person.")
    print("You: \"Psst, hey, do you know a way of getting out of here?\"")
    print("Dude: \"Yeah, might do. Call the guard.\"")
    print("You: \"Are you crazy?!\"")
    print("Dude: \"No, call him.\"")
    print("""You can:
1. Call the guard (and risk you both being killed)
2. Do nothing (and see how it plays out).""")
    while 1:
        room1sub1do = input("\nWhat do you wish to do? : ")
        if room1sub1do == "1":
            print("You call the guard.")
            room1sub2()
        elif room1sub1do == "2":
            print("You wait a little bit.")
            bored = bored - 1
            if bored == 0:
                print("The other person gets sick of waiting and calls the guard for you.")
                room1sub2()
        else:
            print(incorrectgen())
def room1sub2():
    print("-"*79)
    print("The guard shouts out: \"HEY! SHUT THE !@%# UP!\" to you. Nice.")
    print("The guard starts to walk over. The other person prepares himself.")
    print("As the guard kneels down, the other person grabs the guard's head and \nslams it against the cage, killing him.")
    print("He unties himself, and goes to untie you. He tells you to follow him.")
    print("This is the end of the current pre-alpha. Thanks for testing!")
    exit()

splash()
start()
premise()
room1()
