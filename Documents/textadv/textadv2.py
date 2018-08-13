# -*- coding: utf-8 -*-
#notes section:
#do save/load
#put save/quit into all selections
#make score add to save and add saved score to score when continuing the game for a higher score
#in autobattle mode add option to randomly eat bread or drink potion 
#etc.

#Credits:
#Sounds: Microsoft Corporation and Peter Skaven (chord, tada, transition, and loop)

#Importing:
from time import sleep
from random import randint, choice
from winsound import Beep as beep
from os import system, path, remove
from playsound import playsound
import _thread
from platform import system as syscheck
from configparser import ConfigParser
if syscheck() == "Windows":
    runpy = 'py.exe'
    system("mode con: cols=80 lines=25")
    system('CHCP 65001 >nul')
    system('title Untitled Text Game 2 - Beta build 1.2_02')
else:
    runpy = 'python3'

#Variables:
config = ConfigParser()
breadcount = 6    #TEMPORARY
potioncount = 1   #TEMPORARY
trinketcount = 1  #TEMPORARY
money = 50        #TEMPORARY
opphealth = 20    #TEMPORARY
health = 20       #TEMPORARY
strength = 1      #TEMPORARY
templelockout = 0 #TEMPORARY
checkdrop = 0     #TEMPORARY
confid = 0        #TEMPORARY
invalidchar = ['\\','/',':','?','"','<','>','|']
areasel = ""
forestop3load = 0
countdown = 3

#Functions:
def gendata():
    config['UTG2 Save File'] = {'Health': '20',
                                'OppHealth': '20',
                                'Strength': '1',
                                'Bread': '2',
                                'Continue': 'no',
                                'Money': '50',
                                'Score': '0',
                                'TempleLockOut': '0',
                                'CheckDrop': '0',
                                'Confid': '0'}
                                
    config.write(open(name + ".ini",'w'))

def sounds(sound):
    if sound == 0:
        playsound('tada.mp3')
    if sound == 1:
        playsound('chord.wav')
    if sound == 2:
        playsound('loop.mp3')
    if sound == 3:
        playsound('gameover.mp3')
    if sound == 4:
        playsound('spotted.mp3')
    if sound == 5:
        playsound('transition.wav')

def splash():
    _thread.start_new_thread( sounds, (2,) )
    system('cls')
    logo = """
   __  __      __  _ __  __         __
  / / / /___  / /_(_) /_/ /__  ____/ /
 / / / / __ \/ __/ / __/ / _ \/ __  / 
/ /_/ / / / / /_/ / /_/ /  __/ /_/ /  
\_______ /_/\__/_/___/_/\___/\__,_/   
 /_  __/__  _  __/ /_
  / / / _ \| |/_/ __/
 / / /  __/>  </ /_
/_/__\\___\/_/|_|\__/             ___
  / ____/___ _____ ___  ___     |__ \ 
 / / __/ __ `/ __ `__ \/ _ \    __/ / 
/ /_/ / /_/ / / / / / /  __/   / __/  
\____/\__,_/_/ /_/ /_/\___/   /____/  
    """
    print(logo)
    print("Version 1.2_02 Beta")
    print("(C) 2016 Aidan Rayner")
    
    while 1:
        invalid = False
        name = input("Please enter your username: ")
        for x in range(len(invalidchar[0:])):
            if invalidchar[x] in name:
                print("Invalid characters detected: " + invalidchar[x])
                invalid = True
        if len(name) == 0 and not invalid == True:
            print("You can't have a blank username!")
        elif not invalid == True:
            if not path.exists(name + ".ini"):
                open(name + ".ini",'w').close()
                if not path.exists(name + ".ini"):
                    print("ERROR: Data write error has occurred in program! Data CANNOT be saved!")
                    print("This is likely due to an invalid file name.")
                    print("The program has been halted. Press enter to reset.")
                    input("")
                    system(runpy + " textadv2.py")
                    exit()
                print("New user profile created.")
                print("As you are a new user, please take the time to read the help file!\n(Option 4 on the main menu)")
                sleep(5)
            else:
                print("Welcome back, " + name + "!")
                sleep(1)
            return name

def gethelp():
    system('cls')
    print("\n")
    print("-"*79)
    print("Help - Untitled Text Game 2".center(80))
    print("-"*79)
    print("\n")
    print("    Welcome to help.\n\n")
    print("    Supported commands (outside of given prompts):")
    print("    s (save), q (save and quit), stats (health, bread amount, etc)\n")
    print("    General info:")
    print("    This is a text based adventure game based around a JRPG theme.\n    We're currently in alpha, so please report any bugs!!\n")
    input("    Type q to return to the main menu: ")

def leave():
    sure = input("    Are you sure you want to quit? [y/N]: ")
    if sure.lower() == "y":
        print("    Quitting...")
        sleep(1)
        exit()

def scribe():
    system('cls')
    print("\n")
    print("-"*79)
    print("Scribe - Untitled Text Game 2".center(80))
    print("-"*79)
    print("\n")
    print(u"    In a puff of smoke, a Kindle™ tablet (other brands are available)")
    print("    appears in your hand. On the screen are your stats.")
    print("\n")
    print("    Unfortunately for you, the tablet crashes.") ### CHANGE TO SET WHEN YOU LOAD STUFF
    print("    The error message it displays is: \"Load feature not implemented yet.")
    sleep(10)

def score():
    for x in range(100):
        genscore = randint(1,11000)
        print("    Your score is: " + str(genscore) + "     ",end='\r'), sleep(0.02)
    print("    Your score is: " + str(genscore))

def retry():
    print("\n")
    startagain = input("    Would you like to restart? [Y/n]: ") ###SET CONTINUE TO YES HERE!!!
    if startagain.lower() == "n":
        exit()
    else:
        system(runpy + " textadv2.py")
        exit()

def alert():
    system('cls')
    _thread.start_new_thread( sounds, (4,) )
    print(" "*80)
    print("\n\n\n\n\n")
    print("""
                                        __
                                       / /
                                      / / 
                                     /_/  
                                    (_)   """.center(80)), sleep(0.8)
    print("You've been spotted.".center(80)), sleep(0.8)

def menu():
    system('cls')
    print("\n")
    print("-"*79)
    print("Main Menu - Untitled Text Game 2".center(80))
    print("-"*79)
    print("\n    1. Start a new game\n\n    2. Load a saved game\n\n    3. Continue (after death)\n\n    4. Help\n\n    5. Quit\n\n")
    menusel = input("\n\n    Select an option: ")
    return menusel


def selectarea():
    while 1:
        startlist = ['1','2','3']
        system('cls')
        print("\n")
        print("-"*79)
        print("Start a new game - Untitled Text Game 2".center(80))
        print("-"*79)
        print("\n    Where do you want to start, " + name + "?\n\n    1. The Village Town\n\n    2. The Forest\n\n    3. The Nearby Castle")
        areasel = input("\n\n    Select an option: ")
        if areasel in startlist:
            return areasel         
        print("\n    Invalid input.")
        sleep(2)

def loadgame(loadtype):
    if loadtype == "load":
        for x in range(12):
            print("    Loading data |", end='\r'), sleep(0.05)
            print("    Loading data /", end='\r'), sleep(0.05)
            print("    Loading data -", end='\r'), sleep(0.05)
            print("    Loading data \\", end='\r'), sleep(0.05)
        config.read(name + ".ini")
        if len(open(name + ".ini",'r').read()) == 0:
            print("    There is no data to load!")
            sleep(2)
            return False
        for x in range(12):
            print("    Checking data integrity |", end='\r'), sleep(0.05)
            print("    Checking data integrity /", end='\r'), sleep(0.05)
            print("    Checking data integrity -", end='\r'), sleep(0.05)
            print("    Checking data integrity \\", end='\r'), sleep(0.05)
        if not 'UTG2 Save File' in config.sections():
            print("    Data file is invalid. Cannot load save.")
            sleep(2)
            return False
        print("    Data check passed. Your data has been loaded successfully.")
        sleep(2)
    elif loadtype == "read" or loadtype == "check":
        if loadtype == "read":
            loadtype = "Reading"
        else:
            loadtype = "Checking for"
        for x in range(8):
            print("    " + loadtype + " data |", end='\r'), sleep(0.05)
            print("    " + loadtype + " data /", end='\r'), sleep(0.05)
            print("    " + loadtype + " data -", end='\r'), sleep(0.05)
            print("    " + loadtype + " data \\", end='\r'), sleep(0.05)
        config.read(name + ".ini")

def loadarea(place):
    _thread.start_new_thread( sounds, (5,) )
    system('cls')
    print("\n"*9)
    print("-"*79)
    loadtext = "Now loading: " + place
    print(loadtext.center(80))
    print("-"*79)
    sleep(1)

def continuegame():
    loadgame("read")
    if len(open(name + ".ini",'r').read()) == 0:
            print("    There is no data to load!")
    if not 'UTG2 Save File' in config.sections():
        print("    Data file is invalid. Cannot load save.")
        sleep(2)
    elif str(config['UTG2 Save File']['Continue']) == "no":
        _thread.start_new_thread( sounds, (1,) )
        print("    You do not have a continue point to load from.")
        sleep(2)

def town():
    while 1:
        townlist = ['1','2','3','4','5']
        system('cls')
        print("\n")
        print("-"*79)
        print("\n")
        print("    You arrive in the town. There's a lot of people here today.")
        print("    You see a market selling potions, trinkets, and food. Ahead, you")
        print("    see a worried man. There's also a temple nearby.\n")
        print("    What do you wish to do?\n")
        print("    1. Visit the market\n    2. Consult the worried man\n    3. Leave for the forest\n    4. Leave for the castle\n    5. Visit the temple\n")
        townsel = input("    Select an option: ")
        if townsel in townlist:
            return townsel
        print("    Invalid input.")
        sleep(1)

def market():
    global breadcount
    global money
    global potioncount
    global trinketcount
    global strength
    while 1:
        marketlist = ['1','2','3']
        system('cls')
        print("\n")
        print("-"*79)
        print("\n")
        print("    You arrive in the market. On the table is " + str(breadcount) + " loaves of bread, " + str(trinketcount) + " trinket(s)")
        print("    (which 'supposedly' gives you more strength), and " + str(potioncount) + " health potion(s).")
        print("    You reach for your wallet. Inside is " + str(money) + " money.\n")
        print("    What do you wish to buy?\n")
        print("    1. Two loaves of bread (10 money)\n    2. The potion (30 money)\n    3. The trinket (20 money)\n    4. Leave the market")
        marketbuy = input("    Select an option: ")
        if marketbuy == "1":
            if breadcount > 0:
                if money > 9:
                    print("    You purchase two loaves of bread.")
                    money = money - 10
                    breadcount = breadcount - 2
                else:
                    print("    You do not have enough money for this.")
            else:
                print("    The seller has run out of bread, because you bought it all.")
        elif marketbuy == "2":
            if potioncount > 0:  
                if money > 29 :
                    print("    You purchase the potion.")
                    money = money - 30
                    potioncount = potioncount - 1
                else:
                    print("    You do not have enough money for this.")
            else:
                print("    There's no more potions left.")
        elif marketbuy == "3":
            if trinketcount > 0:
                if money > 19:
                    print("    You purchase the trinket.")
                    print("    Your strength has been boosted!!")
                    money = money - 20
                    trinketcount = trinketcount - 1
                    strength = strength + 1
                else:
                    print("    You do not have enough money for this.")
            else:
                print("    There's no more trinkets left.")
        elif marketbuy == "4":
            return "1"
        else:
            print("    Invalid input.")
            sleep(1)
        if marketbuy in marketlist:
            marketask = input("    Anything else? [Y/n]: ")
            if marketask.lower() == "n":
                break

def temple():
    global money
    global health
    global templelockout
    global confid
    templelist = ['1','2','3']
    while 1:
        system('cls')
        print("\n")
        print("-"*79)
        print("\n")
        print("    You enter the temple. A man greets you and offers you a couple of things.")
        print("    For a small fee (20 money) he can boost your health by 15. He also offers")
        print("    you a service for free that boosts your confidence, apparently.\n")
        print("    You have " + str(money) + " money in your wallet.")
        print("    What do you wish to do?\n")
        print("    1. Boost health (20 money)")
        print("    2. Boost confidence (0 money)")
        print("    3. Leave the temple\n")
        templesel = input("    Select an option: ")
        if templesel in templelist:
            if templesel == "1":
                if money > 19:
                    if templelockout == 0:
                        print("    Your health was boosted.")
                        health = health + 15
                        money = money - 20
                        templelockout = 1
                    else:
                        print("    You've already been here today. You can't do it again.")
                else:
                    print("    You cannot afford this.")
            elif templesel == "2":
                print("    Nothing happens. You do feel better, though.")
                confid = confid + 1
                if confid == 25:
                    print("    \"You've got some dedication. I like it.\" the man says.")
                    print("    You're given another 5 health.")
                    health = health + 5
            elif templesel == "3":
                return True
            templeask = input("    Anything else? [Y/n]: ")
            if templeask.lower() == "n":
                return True
        else:
            print("    Invalid input.")
        
    
def man():
    system('cls')
    print("\n\n")
    print("    You consult the man. He explains that there's a huge monster not too")
    print("    far away that's scaring the locals. Your task is to kill it.")
    print("\n")
    print("    You thank the man and return to the town.")
    sleep(10)
       
def forest():
    while 1:
        forestlist = ['1','2','3','4']
        system('cls')
        print("\n")
        print("-"*79)
        print("\n")
        print("    You wander off into the forest. Without a map, you become a bit lost.")
        print("    You think you can see something off into the distance, but you're not")
        print("    sure what it is.\n")
        print("    What do you wish to do?\n")
        print("    1. Investigate the odd looking distant...thing\n    2. Wander around the forest a bit more\n    3. Sit and wait for a bit and see if anyone passes through.\n    4. Go back the way you came in hope you find where you started from.\n")
        forestsel = input("    Select an option: ")
        if forestsel in forestlist:
            return forestsel
        print("    Invalid input.")
        sleep(1)

def forestop1():
    alert()
    system('cls')
    
def forestop2():
    system('cls')
    print("\n")
    print("-"*79)
    print("\n")
    print("    You wander off even further. You become even more lost at this point.")
    print("    You turn around to see the huge monster right behind you. You've got")
    print("    no chance of getting away from it now.")
    print("\n\n")
    input("    Are you ready? [y/n]: ")
    alert()

def forestop3():
    global countdown
    if countdown == 3:
        print("    You wait a bit.")
    if countdown == 2:
        print("    You wait a bit longer.")
    if countdown == 1:
        print("    You wait quite a long time.")
    if countdown == 0:
        death(4)
    countdown = countdown - 1

def castle(castlecheck):
    global money
    system('cls')
    print("\n")
    print("-"*79)
    print("\n")
    if castlecheck < 1:
        print("    You arrive at the castle. There's no one here. You find some money on")
        print("    the ground, which you take. You find a loaf of bread by the side. It")
        print("    looks a bit old, but it's still edible. You take this as well.")
        print("\n\n")
        print("    You've gained: 1 bread and 50 money.")
        print("    You return back to the town as there's nothing else to do.")
        money = money + 50
        sleep(10)
    else:
        print("   You've been here before. There's still no-one here and there's nothing")
        print("   left to take. You return back to the town again.")
        sleep(5)

def death(deathvar):
    global health
    global opphealth
    for x in range(20):
        print("\n"), sleep(0.1)
    system('cls')
    print("\n")
    _thread.start_new_thread( sounds, (3,) )
    if deathvar == 1:
        print("    Unfortunately for you, the monster has killed you off in a rather")
        print("    spectacular fashion. You have failed your mission, and the rest of")
        print("    your town, friends, family, and the world.")
    if deathvar == 2:
        print("    You valiantly try to fight the being. Unfortunately for you, it")
        print("    simply ignores your strike and looks over to you. In a flash, it")
        print("    swallows you whole, killing you instantly.")
    if deathvar == 3:
        print("    You attempt to comfort the being. The problem is though, it wasn't")
        print("    in the best mood, and it didn't feel like befriending anyone.")
        print("    It looked over to you, and before you could sneeze, it swallowed")
        print("    you whole. Sorry about that. :/")
    if deathvar == 4:
        print("    You waited so long that you dehydrated to death. I don't quite")
        print("    understand why you did that, but there we are I suppose.")
        print("    Try not to do that again, moron.")
    print("\n\n\n\n")
    endtext = "    Game over."
    for x in range(len(endtext)):
        print(endtext[0:x+1], end='\r'), sleep(0.2)
    print("\n\n\n\n")
    score()
    retry()

def draw():
    global health
    global opphealth
    for x in range(20):
        print("\n"), sleep(0.1)
    system('cls')
    print("\n")
    _thread.start_new_thread( sounds, (3,) )
    print("    Uh...well, this is awkward. You both died at the same time.")
    print("    I guess you didn't win but at the same time you didn't lose...")
    print("    I've got no idea. Sorry. Probably best if you retry.")
    print("\n\n\n\n")
    endtext = "    You ????"
    for x in range(len(endtext)):
        print(endtext[0:x+1], end='\r'), sleep(0.2)
    for x in range(10):
        print("    ????????", end='\r'), sleep(0.05)
        print("    ???a!d??", end='\r'), sleep(0.05)
        print("    ????????", end='\r'), sleep(0.1)
        print("    ????????", end='\r'), sleep(0.05)
        print("    ??!!££$?", end='\r'), sleep(0.05)
        print("    sfD??!??", end='\r'), sleep(0.2)
        print("    !!!!!!!!", end='\r'), sleep(0.05)
        print("    ??$%^*??", end='\r'), sleep(0.05)
        print("    !!!!!!!!", end='\r'), sleep(0.15)
        print("    !!!!!!!!", end='\r'), sleep(0.05)
    endtext = "    ERROR: Unable to determine outcome."
    for x in range(len(endtext)):
        print(endtext[0:x+1], end='\r'), sleep(0.1)    
    print("\n\n\n\n")
    score()
    retry()

def win(winvar):
    sleep(1)
    for x in range(20):
        print("\n"), sleep(0.1)
    system('cls')
    print("\n")
    if winvar == 1:
        print("    You strike the being. Your quick reflexes manage to get you")
        print("    up to its head. You repeatedly strike its neck with your sword")
        print("    until it cuts through. The being crashes to the ground as you")
        print("    cart off its head using a barrow you found nearby back to the")
        print("    town, asking for directions on the way.\n")
        print("    As you arrive in town, people cheer and clap. You're given a")
        print("    free drink, and you choose to pin the head in the centre of")
        print("    the town.\n\n")
    if winvar == 2:
        print("    You ask it to move out of the way to avoid scaring everyone,")
        print("    but you explain you'll come and see it as much as you can.")
        print("    The being happily obliges and strolls off out of the way.")
        print("    You hug the being, and run back to the town (after jumping")
        print("    up on its head to see where to go.\n")
        print("    You arrive in town and explain the being is no longer a threat.")
        print("    You are treated to a free drink and crowned the town's hero.\n\n")
    if winvar == 3:
        print("    You convince it to follow you home, sitting atop its head to")
        print("    find your way back. As you approach the town, the townsfold erupt")
        print("    into a frenzy. You shout out \"Don't worry, I have tamed the beast!")
        print("    Everyone please calm down!\". To your surprise, the townsfolk actually")
        print("    liusten to you and start to calm down. They congratulate you and treat")
        print("    you to a free drink. You take the being home and keep it as your pet.\n")
        petname = input("    What do you wish to call your new pet? : ")
        system('cls')
        print("\n")
        print("    Your pet, " + petname + ", is very happy with its new name.\n\n")
    _thread.start_new_thread( sounds, (0,) )
    endtext = "    You win!"
    for x in range(len(endtext)):
        print(endtext[0:x+1], end='\r'), sleep(0.1)
    print("\n\n\n\n")
    score()
    retry()

def autobattle():
    global health
    global opphealth
    global strength ###CHANGE TO LOAD FROM DATA!!!###
    attack = ""
    attack1 = ""
    while 1:
        attackextra = 0
        if strength >= 2:
            attackextra = randint(1,4)
        attacksel = randint(1,6)
        if attacksel == 1:
            attack1 = "Hit to Player: 1 damage!          "
            attack = ""
            health = health - 1
        if attacksel == 2:
            attack = "Hit to Enemy: 1 damage!           "
            attack1 = ""
            opphealth = opphealth - 1
        if attacksel == 3:
            attack = "You missed! No damage done.       "
            attack1 = ""
        if attacksel == 4:
            attack1 = "The enemy missed! No damage done. "
            attack = ""
        if attacksel == 5 or attackextra == 3:
            attack1 = "CRITICAL HIT TO PLAYER! 3 damage!!"
            attack = ""
            health = health - 3
        if attacksel == 6:
            attack = "CRITICAL HIT TO ENEMY! 3 damage!! "
            attack1 = ""
            opphealth = opphealth - 3
        system('cls')
        print("\n")
        print("    The battle has begun.")
        print("    Your current health is: " + str(health) + " and your opponent's is: " + str(opphealth) + "\n")
        print("    Your current attack: " + attack + "\n")
        print("    Enemy's current attack: " + attack1 + "\n")   
        if health < opphealth:
            status = "losing."
        elif health > opphealth:
            status = "winning."
        else:
            status = "drawing."
        print("    You're currently " + status + "\n")
        print("    The game is running automatically. Please wait.")
        if health <= 0:
            death(1)
        if opphealth <= 0:
            win(1)
        sleep(1)

def manualbattle():
    global health
    global opphealth
    attack = ""
    attack1 = ""
    while 1:
        system('cls')
        print("\n")
        print("    The battle has begun.")        
        print("    Your current health is: " + str(health) + " and your opponent's is: " + str(opphealth) + "\n")
        print("    Your previous attack: " + attack + "\n")
        print("    Enemy's previous attack: " + attack1 + "\n")    
        if health < opphealth:
            status = "losing."
        elif health > opphealth:
            status = "winning."
        else:
            status = "drawing."
        print("    You're currently " + status + "\n")
        if health <= 0:
            death(1)
        if opphealth <= 0:
            win(1)
        print("    You can: attack (a), defend (d), or do nothing (n).\n")
        manualsel = input("    Select an option: ")
        if manualsel.lower() == "a":
            randomsel1 = randint(1,4)
            if randomsel1 == 1 or randomsel1 == 3:
                attack = "Hit to Enemy: 1 damage!          "
                opphealth = opphealth - 1
            if randomsel1 == 2:
                attack = "You missed! No damage done.       "
            if randomsel1 == 4:
                attack = "CRITICAL HIT TO ENEMY! 3 damage!! "
                opphealth = opphealth - 3  
        if manualsel.lower() == "n":
            attack = "You do nothing."
        if manualsel.lower() == "d":
            attack = "You attempt to defend yourself...somehow."
        randomsel2 = randint(1,5)
        if randomsel2 == 1:
            attack1 = "CRITICAL HIT TO PLAYER! 3 damage!!"
            health = health - 3
        if randomsel2 == 2 or randomsel2 == 3:
            attack1 = "Hit to Player: 1 damage!          "
            health = health - 1
        if randomsel2 == 4 or randomsel2 == 5:
            attack1 = "The enemy missed! No damage done. "
        print(randomsel2)

def fight():
    randomdeath = randint(1,50)
    fightlist = ['1','2','3']
    while 1:
        system('cls')
        print("\n")
        print("-"*79)
        print("\n")
        print("    With sword in hand, you prepare to fight the being. It doesn't look")
        print("    like too much, until it gets up. It's huge. Seriously huge.")
        print("    Still, you figure you might as well try.\n")
        print("    What do you wish to do?")
        print("    1. Flee\n    2. Try and fight it\n    3. Comfort the being\n")
        fightsel = input("    Select an option: ")
        if fightsel in fightlist:
            if not randomdeath == 25:
                if fightsel == "1":
                    print("    There's no running away from this battle. Sorry.")
                    sleep(2)
                if fightsel == "2":
                    autosel = input("    Do you want to fight manually or have the game do it? [auto/manual]: ")
                    if autosel.lower() == "auto":
                        autobattle()
                    else:
                        manualbattle()
                if fightsel == "3":
                    comfort()
            else:
                death(2)
        print("    Invalid input.")
        sleep(2)

def comfort():
    while 1:
        comfortlist = ['1','2']
        randomdeath = randint(1,2)
        if randomdeath == 2:
            death(3)
        else:
            system('cls')
            print("\n")
            print("-"*79)
            print("\n")
            print("    You call to the being. As it turns to you, you place your")
            print("    sword on the ground. \"I don't intend to hurt you. You look")
            print("    sad today, what's happened?\" you say. The being looks at")
            print("    you glumly. It makes a strange noise as it slumps its head by")
            print("    your side. You pet its head as its ears rise. It starts to smile.")
            print("    You continue to do this, and the being becomes extremely happy.\n")
            print("    What do you wish to do?\n")
            print("    1. Ask it to move elsewhere to avoid scaring the townsfolk")
            print("    2. Take it home as a pet (and explain to the townsfolk it's harmless)\n")
            comfortsel = input("    Select an option: ")
            if comfortsel in comfortlist:
                if comfortsel == "1":
                    win(2)
                if comfortsel == "2":
                    win(3)
            print("    Invalid input.")
            sleep(2)
                
#Runtime code:

name = splash()
while 1:
    option = menu()
    if option == "1":
        loadgame("check")
        config.read(name + ".ini")
        if 'UTG2 Save File' in config.sections():
            _thread.start_new_thread( sounds, (1,) )
            print("    WARNING! Save file detected! Continuing will overwrite your")
            confirm = input("    save PERMANENTLY! Are you sure you want to continue? [y/N]: ")
            if confirm == "y":
                remove(name + ".ini")
                open(name + ".ini",'w').close()
                gendata()
            else:
                continue
        else:
            gendata()
        areasel = selectarea()
        break
    elif option == "2":
        loadgame("load")
    elif option == "3":
        continuegame()
    elif option == "4":
        gethelp()
    elif option == "5":
        leave()
    else:
        print("\n    Invalid input.")
        sleep(2)
while 1:
    if areasel == "1":
        loadarea("The Town")
        townsel = town()
        if townsel == "1":
            loadarea("The Market")
            loadmarket = market()
            if loadmarket == "1":
                areasel = loadmarket
        elif townsel == "2":
            man()
        elif townsel == "3":
            areasel = "2"
        elif townsel == "4":
            areasel = "3"
        elif townsel == "5":
            loadarea("The Temple")
            temple()
    if areasel == "2":
        if forestop3load == 0:
            loadarea("The Forest")
        forestsel = forest()
        if forestsel == "1":
            forestop1()
            fight()
        elif forestsel == "2":
            forestop2()
            fight()
        elif forestsel == "3":
            forestop3()
            forestop3load = 1
            sleep(2)
        elif forestsel == "4":
            areasel = "1"
    if areasel == "3":
        loadarea("The Nearby Castle")
        castle(checkdrop)
        checkdrop = checkdrop + 1
        areasel = "1"
    if areasel == "4":
        loadarea("Previous Save")






