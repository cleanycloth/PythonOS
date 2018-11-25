#!/usr/bin/python

#notes:
#look at converting system files to use ConfigParser <<< important
#make a dependencies checker
#make filelist for runtests and checkfiles one text file

#Load modules and set variables required for defined functions:
from time import sleep, asctime
from os import path, system, getcwd, chdir, remove, rename
from platform import system as osdetect
if osdetect() == "Windows":
    from winsound import Beep as beep
else:
    def beep(thinga, thingb):
     print("", end='\r')
from random import randint
from getpass import getpass
from glob import glob
from webbrowser import open as webopen
from playsound import playsound
import _thread
try:
    from loadanimation import load
    from login import login
    from logos import logo, startlogo
except:
    load = ""
    login = ""
    logo = ""
    startlogo = ""

rand = 0
firstboot = 0
sysdir = getcwd()
owd = getcwd()
owd2 = ""
version = "1.9"
build = "25/11/18 @ 10:01am"
year = "2015-2018"
compname = "pOS"
filelist = ['safeshutdown.txt','programlist.txt','Documents/m8ballusernames.txt','Documents/m8ballresults.txt','currentuser.txt','fastboot.txt','lastlogin.txt']
soundwarning = 0
if osdetect() == "Windows":
    runpy = 'py.exe'
    runtext = 'k.exe '
    runprog = "start"
    readtext = "more"
    helpfile = " khelp.hlp"
else:
    runpy = 'python3'
    runtext = 'nano ' + str(owd2)
    runprog = ""
    readtext = "head"
    helpfile = "nhelp.hlp"

#Define necessary functions:
def writefiles(filename, data):
    file = open(filename, "w")
    file.write(data), file.close()
def workdir():
    global owd1
    owd1 = getcwd()
    chdir(owd)  
def wintitle():
    if osdetect() == "Windows":
        system('title PythonOS VM - Version ' + version + ' (C) RotoWare ' + year) # This sets the command line window title.
wintitle()
def screenclear():
    if osdetect() == "Windows":    
        system('cls')
        system('color 07')
    else:
        system('clear')
def createuser():
    owd1 = getcwd()
    chdir(owd)
    while 1:
        username = input("Enter a username: ")
        if path.exists("Users/" + username + ".limited") or path.exists("Users/" + username + ".admin"):
            print("This username already exists.")
        elif username == "return":
            if noadmin == 1:
                print("This username cannot be used as it is a system keyword.")
            else:
                print("Returning to prompt.")
                username = "return1"
                break
        elif len(username) == 0:
            print("Username cannot be blank.")
        else:
            break
    if not username == "return1":
        while 1:
            password = getpass(prompt='Enter a password. Note: input is hidden for security. : ')
            if password == "return":
                if noadmin == 1:
                    print("This password cannot be used as it is a system keyword.")
                else:
                    print("Returning to prompt.")
                    break
            elif len(password) == 0:
                print("Password cannot be blank.")
            else:
                break
        if noadmin == 0 and not password == "return":
            while 1:
                permissions = input("Enter a permission level (admin or limited): ")
                if permissions.lower() == "admin" or permissions.lower() == "limited":
                    break
                print("Invalid input. Try again.")
        if noadmin == 1 and not password == "return":
            permissions = "admin"
            print("Creating administrator user.")
        if not password == "return":
            userfile = "Users/" + username + "." + permissions
            print("\nUser created.\n")
            writefiles(userfile, password)
            chdir(owd1)
def checkfiles():
    #Checks for files missing, and stops the OS from loading if any are.
    system(runpy + ' checkfiles.py')
    if open('shutdown.txt').read() == "1":
        writefiles("shutdown.txt", "0")
        exit()            
def sounds(sndgrp):
    try:
    #Defines the soundset for the OS. Sound group 2 does not work under linux but instead silently passes through.
        workdir()
        if sndgrp == 0:
            playsound('Sounds/start.wav')
        elif sndgrp == 1:
            playsound('Sounds/shut.wav')
        elif sndgrp == 2:
            beep(800, 500), beep(1200, 500)
        elif sndgrp == 3:
            playsound('Sounds/logoff.wav')
        elif sndgrp == 4:
            playsound('Sounds/logon.wav')
        elif sndgrp == 5:
            playsound('Sounds/uac.wav')
        chdir(owd1)
    except KeyboardInterrupt:
        exit()
def permerror():
    _thread.start_new_thread( sounds, (5,) )
    print("\nYou do not have the required permissions to run this command.\n")
    
#Main runtime code starts here
screenclear()
try:
    fast = open("fastboot.txt").read()
except:
    fast = "0"
if not "1" in fast:
    chdir(sysdir)
    if not path.exists("bios.py"):
        print("\n\nBIOS failure detected. The BIOS file needs to be reinstalled.\n\nSystem halted.")
        print("\nPress Control+C to restart.")
        while 1:
            for x in range(1,4):
                sounds(2)
            sleep(1)
    system(runpy + ' bios.py')
    sleep(1)
    writefiles("shutdown.txt","0")
    screenclear()
    sleep(2)
    if not path.exists("checkfiles.py"):
        print("PythonOS cannot validate the required files needed to start.\nReplace \"checkfiles.py\" and press enter to restart.")
        input("")
        remove("lock")
        exit()
    checkfiles()
    startlogo()
    for x in range(len(filelist)):
        if not path.exists(filelist[x]):
            firstboot = firstboot + 1
            if filelist[x] == "safeshutdown.txt":
                writefiles(filelist[x],"1")
            elif filelist[x] == "fastboot.txt":
                writefiles(filelist[x],"0")
            else:
                writefiles(filelist[x],"")
    if firstboot == len(filelist):
        print("Preparing PythonOS for first time boot, please wait.".rjust(66), end='\r'), sleep(4)
        screenclear()
        startlogo()
    randstart = randint(4,7)
    print("(         )".rjust(45), end='\r'), sleep(0.5)
    for x in range(randstart):
        if not "1" in open("safeshutdown.txt").read():
            load(), load()
            screenclear()
            system(runpy + ' scandisk.py')
            writefiles("safeshutdown.txt","1")
            screenclear()
            startlogo()
        load()

writefiles("safeshutdown.txt","0")
sleep(0.5)
screenclear()
sleep(1)
writefiles("fastboot.txt","0")
print("Welcome, to..."), sleep(0.2)
logo()
_thread.start_new_thread( sounds, (0,) )
print("\nVersion " + version + " Beta - Copyright RotoWare " + year), sleep(0.5)
print("\nBuild Date: " + build), sleep(0.5)
if len(open("lastlogin.txt").read()) == 0:
    print("\nLast login date: Unknown")
else:
    print("\nLast login date: " + open("lastlogin.txt").read())
print("Current time is", asctime(), "\n"), sleep(0.5)
res = 0
loggedout = 1
noadmin = 1
if not path.exists("Users/public.limited"):
    createuser()
    userfile = "Users/public.limited"
    password = ""
    writefiles(userfile, password)
noadmin = 0
while 1:
    wintitle()
    sleep(0.1)
    if loggedout == 1:
        chdir(sysdir)
        login()
        user = open('currentuser.txt').read()
        writefiles("lastlogin.txt",asctime())
        _thread.start_new_thread( sounds, (4,) )
    if not path.exists(owd + "/Users/" + user):
        print("\n" + "-"*36 + "WARNING!" + "-"*36)
        print("Illegal permission level change detected. Reverting changes.")
        print("-"*36 + "WARNING!" + "-"*36 + "\n")
        workdir()
        chdir("Users")
        try:
            if ".admin" in user:
                rename(user1 + ".limited", user)
            else:
                rename(user1 + ".admin", user) 
        except:
            print("Error changing permissions. The user may have been deleted.")
        chdir(owd1)
    if not res == 1:
        workdir()
        chdir(owd1)
        if ".admin" in user:
            user1 = user.replace(".admin", "")
        else:
            user1 = user.replace(".limited", "")
        main = input(user1 + "@" + compname + " | " + owd1 + ">")
        loggedout = 0
    if "play" in main[0:4]:
        main = main.replace(" ","").replace("play","").replace("_"," ")
        if len(main) == 0:
            main = input("Please specify a sound to play: ")
        def s():
            try:
                print("Playing sound file: \"" + main + "\"")
                playsound(main)
            except:
                print("Unable to play the sound.")
        _thread.start_new_thread( s, () )
    elif main.replace(" ","") == "":
        print("",end='\r')
    elif main == "cortana":
        workdir()
        system(runpy + ' cortana.py')
        chdir(owd1)
    elif main == "rootdir":
        chdir(owd)
    elif main == "py":
        system(runpy)
    elif main == "time" or main == "date":
        print(asctime())
    elif "search" in main[0:6]:
        testsearch = main.replace(" ","")
        if testsearch == "search":
            testsearch = input("Please enter a search term: ")
            main = main + " " + testsearch
        main = main.replace(" ", "+")
        main = main.replace("search", "",1)
        webopen('https://www.google.co.uk/?gws_rd=ssl#q=' + main)
    elif main == "listvar":
        print("Global variables: ", globals())
    elif main == "scandisk":
        workdir()
        writefiles("safeshutdown.txt","1")
        screenclear()
        system(runpy + ' scandisk.py')
        chdir(owd1)
        writefiles("safeshutdown.txt","0")
        screenclear()
    elif main == "help":
        workdir()
        chdir('Documents')
        owd2 = owd + "\\"
        system(runtext + 'pythonoshelp.hlp')
        chdir(owd1)
    elif main == "help edit":
        workdir()
        chdir('Documents')
        owd2 = owd + "\\"
        system(runtext + helpfile)
        chdir(owd1)
        main = ""
    elif "edit" in main[0:4]:
        main = main.replace(" ","")
        if main == "edit":
            main = input("Please specify a file name: ")
        workdir()
        chdir('Documents')
        owd2 = owd + "\\"
        main = main.replace("edit", "")
        system(runtext + "\"" + str(owd2) + main + "\"")
        chdir('..')
        chdir(owd1)
    elif main == "ver":
        print("PythonOS Version " + version + " Beta")
    elif main == "logo":
        logo()
    elif main == "list programs":
        workdir()
        system(readtext + ' programlist.txt')
        print("\n")
        chdir(owd1)
    elif main == "list commands":
        workdir()
        system(readtext + ' commands.lst')
        chdir(owd1)
    elif main == "list users":
        owd1 = getcwd()
        chdir(owd)
        chdir("Users")
        system('dir')
        chdir(owd1)
    elif "dir" in main or main == "ls":
        system('dir')
    elif main == "cd..":
        chdir("..")
    elif "cd " in main:
        main = main.replace ("cd ", "")
        try:
            chdir(main)
        except:
            print("Unable to change directory.")
    elif main == "magic 8 ball":
        owd1 = getcwd()
        chdir(owd)
        chdir('Documents')
        system(runpy + ' m8b5.py')
        chdir(owd1)
    elif main == "textadv":
        owd1 = getcwd()
        chdir(owd)
        chdir('Documents/textadv')
        system(runpy + ' textadv2.py')
        chdir(owd1)
    elif main == "runtests":
        owd1 = getcwd()
        chdir(owd)
        system(runpy + ' runtests.py')
        chdir(owd1)
    elif main == "convert":
        owd1 = getcwd()
        chdir(owd)
        system(runpy + ' convert.py')
        chdir(owd1)
    elif main == "unit1test":
        owd1 = getcwd()
        chdir(owd)
        chdir('Documents')
        system(runpy + ' unit1test.py')
        chdir(owd1)
    elif main == "clear" or main == "cls":
        screenclear()
    elif "apt-get install " in main[0:16] or "sudo apt-get install " in main[0:21]:
        print("This command is deprecated. Please use apt install instead.")
    elif "apt install " in main[0:12] or "sudo apt install " in main[0:17]:
        if ".limited" in user:
            permerror()
        else:
            main = main.replace("sudo apt install ", "")
            main = main.replace("apt install ", "")
            if len(main) == 0:
                print("You need to specify the program you want to install first.")
            else:
                for x in range(1,101):
                    print("Checking repositories...(" + str(x) + "%)", end='\r')
                    sleep(0.02)
                print("")
                x = 0
                rand1 = randint(0,20)
                for x in range(1,101):
                    print("Downloading", main, "from http://repositories.pythonos.net... (" + str(x) + "%)", end='\r')
                    sleep(rand1/100)
                owd1 = getcwd()
                chdir(owd)
                file3 = open('programlist.txt', "a")
                file3.write(main), file3.write(", "), file3.close()  
                print("\nExtracting and setting up", main, end='\r')
                if rand1 < 10:
                    sleep(rand1)
                else:
                    sleep(rand1/10)
                print("Extracting and setting up", main, "complete.")
                chdir(owd1)
    elif "apt-get install" in main[0:15] or "sudo apt-get install" in main[0:20]:
        print("You need to specify the program you want to install first.")
    elif "open" in main[0:4]:
        workdir()
        main = main.replace("open ", "")
        if main in open("programlist.txt").read():
            arg = input("Enter any required arguments, blank for none: ")
            print("Starting", main + " with arguments: \"" + arg + "\".")
            chdir(owd1)
            system(runprog + " " + main + " " + arg)
        else:
            print("Program not installed. Run apt-get to install it.")
        chdir(owd1)
    elif main == "shutdown" or main == "exit":
        print("\nBroadcast from " + user1 + "@" + compname + " (pts/0) (" + asctime() + ")")
        print("\nThe system is going down NOW!")
        chdir(owd)
        _thread.start_new_thread( sounds, (1,) )
        sleep(2)
        print("\nPowering off...")
        remove("lock")
        writefiles("safeshutdown.txt","1")
        writefiles("shutdown.txt","1")
        remove
        sleep(0.5)
        exit()
    elif main == "reboot" or main == "restart" or main == "fastreboot":
        print("\nBroadcast from " + user1 + "@" + compname + " (pts/0) (" + asctime() + ")")
        print("\nThe system is going down for reboot NOW!")
        chdir(owd)
        _thread.start_new_thread( sounds, (1,) )
        sleep(3)
        if not res == 1:
            remove("lock")
            writefiles("safeshutdown.txt","1")
            writefiles("fastboot.txt","0")
        sleep(0.2)
        if main == "fastreboot":
            screenclear()
            print("PythonOS is restarting...")
            sleep(2)
            writefiles("fastboot.txt","1")
        exit()
    elif main == "reset":
        if ".limited" in user:
            permerror()
        else:
            print("\n" + "-"*36 + "WARNING!" + "-"*36)
            sure = input("Are you sure you want to reset PythonOS? This will delete all text files in the PythonOS directory and all users.\nConfirm by typing \"yes\" (w/o quotes): ")
            if sure == "yes":
                print("Resetting PythonOS, please wait...",end='\r')
                chdir(owd)
                for x in range(len(filelist)):
                    if path.exists(filelist[x]):
                        remove(filelist[x])
                remove("lock")
                chdir("Users")
                userlist = glob("*.limited")
                for f in userlist:
                    remove(f)
                userlist = glob("*.admin")
                for f in userlist:
                    remove(f)
                sleep(3)
                print("PythonOS has been reset. System will reboot.")
                chdir(owd)
                sleep(2)
                res = 1
                main = "reboot"
            else:
                print("Returning to prompt.")
    elif main == "logout":
        print("\nLogging out.\n")
        _thread.start_new_thread( sounds, (3,) )
        loggedout = 1
    elif main == "createuser":
        if ".limited" in user:
            permerror()
        else:
            createuser()
    elif main == "deleteuser":
        password = ""
        if ".limited" in user:
            permerror()
        else:
            owd1 = getcwd()
            chdir(owd)
            while 1:
                userdel = input("Enter a username to delete. ")
                if userdel == user1:
                    print("You cannot delete the current user.")
                elif userdel == "public":
                    print("You cannot delete the public user.")
                elif path.exists("Users/" + userdel + ".limited"):
                    userdel1 = userdel + ".limited"
                    break
                elif path.exists("Users/" + userdel + ".admin"):
                    userdel1 = userdel + ".admin"
                    break
                elif userdel == "return":
                    password = "return"
                    break
                else:
                    print("Incorrect username. Try again.")
            while 1:
                if password == "return":
                    break
                password = getpass(prompt='Enter the password of the user. ')
                if password == "return":
                    break
                if not password == open('Users/' + userdel1).read():
                    print("Incorrect password. Try again.")
                else:
                    break
            if not password == "return":
                ask = input("Are you sure you want to delete user " + userdel + "? [yes/no]: ")
                if ask == "yes":
                    remove("Users/" + userdel1)
                    print("User removed.")
            else:
                print("Returning to prompt.")
            chdir(owd1)
    else:
        print("Unknown command. Type \"help\" for a list of commands.")
print("Uh oh, you shouldn't see me. If you can, something is really badly wrong.")
print("Inspection of the code is required. System halted.")
print("\nPress enter to restart.")
input("")
exit()
