#!/usr/bin/python
# The Magic 8 Ball, programmed by Aidan Rayner with optimization and some extra features by Nathan Barrall (choice feature).
from random import choice                                                                                                                                                               # Imports random from choice
from time import sleep, asctime                                                                                                                                                         # Imports asctime and sleep from time
from os import path, remove, system                                                                                                                                                     # Imports path and remove from os
from platform import platform                                                                                                                                                           # Imports platform
from platform import system as syst
from sys import exit                                                                                                                                                                    # Imports exit from sys
from getpass import getpass																				# Imports getpass from getpass
from webbrowser import open as webopen
def savefile():                                                                                                                                                                         # Creates a function (savefile()) with the code attached to it listed below
        game = open("m8ballresults.txt", "a")                                                                                                                                           # Opens results file for editing
        if c == "":
            game.write(start), game.write("\n"), game.write(ask), game.write("\n\n"), game.close(), print("\nYour data has been saved.")                                                # Saves data to a list in a text document, and prints the conformation text.
        else:
            game.write(start), game.write("\n"), game.write(ask), game.write("\n"), game.write(c), game.write("\n\n"), game.close(), print("\nYour data has been saved.")
        sleep(1)                                                                                                                                                                        # Waits for two seconds
while 1:                                                                                                                                                                                # Initiates an infinite loop, until broken.
    c = ""
    debug1 = 0                                                                                                                                                                          # Sets debug1 to 0, simultaneously creating a variable.
    if syst() == 'Windows':                                                                                                                                                             # Checks if the operating system is Windows. If it is, it runs the 'cls' command. If not, it runs the 'clear' command. This clears the screen.
        system('cls')
    else:
        system('clear')
    while 1:
        print("Magic 8 Ball v5.9 RC5".rjust(79))
        if not path.exists("m8ball.password"):                                                                                                                                          # Checks for the password file
            print("Password file not found. Debug mode will be unavailable.")
        if not path.exists("m8ballresults.txt"):                                                                                                                                        # Checks for the results file
            file = open('m8ballresults.txt', "w")                                                                                                                                       # Creates new results file if not found by opening a new file, then closing it.
            print("New results file generated.")
            file.close()
        if not path.exists("m8ballusernames.txt"):                                                                                                                                      # Checks for the usernames file
            file2 = open('m8ballusernames.txt', "w")
            print("New usernames file generated.")                                                                                                                                      # If not found, it generates a new one.
            file2.close()
        print(), print("Hello! Welcome to Magic 8 Ball - Python Edition!")
        start = input("What is your name? : ")                                                                                                                                          # Asks for your name
        if start.lower() == "your mum":
            print("Haha, very funny. Original.")
            break
        if start.lower() == "you're mum":
            print("Nooo, YOU'RE a mum :D :D")
            break
        if start.lower() == "debug":                                                                                                                                                    # If debug is entered for the username field, it activates the debug mode.
            if not path.exists("m8ball.password"):                                                                                                                                      # Checks if the password file does not exist. If it doesn't, it disallows entry and restarts the program.
                print("Debug mode is unavailable because the password file is missing.\nReplace the file, and restart.")
                break
            while 1:
                print()
                passw = getpass(prompt='Enter the password. ')                                                                                                                          # Asks for the password, while not showing the entered characters.
                passw1 = open('m8ball.password', "r")                                                                                                                                   # Checks if the password is right
                if not passw in passw1:
                    print("\nIncorrect password. Try again.")
                else:
                    print("\nYou have entered Magic 8 Ball debug mode.")
                    while 1:
                        print("What would you like to do?\n    1. Delete m8ballresults.txt file\n    2. Delete m8ballusernames.txt file\n    3. Delete both files")                     # Asks the user what they want to do.
                        debug1 = input("    4. View results file\n    5. View usernames file\n    6. Exit\nSelect an option: ")
                        if debug1 == "1":
                            print("Results file deleted."), remove("m8ballresults.txt")                                                                                                 # Deletes the results file
                            break                                                                                                                                                       # Breaks out of loop
                        elif debug1 == "2":
                            print("Usernames file deleted."), remove("m8ballusernames.txt")                                                                                             # Deletes the usernames file
                            break
                        elif debug1 == "3":
                            print("Usernames and results files deleted."), remove("m8ballusernames.txt"), remove("m8ballresults.txt")                                                   # Deletes usernames and results file.
                            break
                        elif debug1 == "4":
                            print("Opening file...")
                            system('start notepad.exe m8ballresults.txt')
                            break
                        elif debug1 == "5":
                            print("Opening file...")
                            system('start notepad.exe m8ballusernames.txt')
                            break
                            break
                        elif debug1 == "6":
                            print("Exiting...")
                            break
                        else:
                            print("\nIncorrect input. Try again.\n"), sleep(2)
                    break                                                                                                                                                               # Breaks out of debug loop.
        if debug1 == "1" or debug1 == "2" or debug1 == "3" or debug1 == "4" or debug1 == "5" or debug1 == "6" or debug1 == "7":                                                         # If debug was used, it breaks out of the loop again, which leads to the restart option. If not, it proceeds.
            break
        if start in open('m8ballusernames.txt').read():                                                                                                                                 # Checks if the current user has logged in before. If they have, the program prints the next line and continues.
            print("Welcome back! I see you seek more advice.")
        else:
            qu = input("Thank you for signing in for the first time.\nYour name, question, and answer will be saved to a file in plaintext. \nDo you accept? [y/N] ")                   # Asks the user if they want to store their name in plaintext. This is required to use the program.
            if qu == "y":
                file3 = open('m8ballusernames.txt', "a")
                file3.write(start), file3.write(", "), file3.close()                                                                                                                    # Saves the username to a file
                print("Thank you. Your username has been saved.")
            else:
                print("You have not accepted the EULA. Magic 8 Ball cannot continue.")
                break
        ask = input("\nAsk me a question! Any question; I don't mind. : ")                                                                                                              # Asks the user for a question.
        print()
        if ask == "What's the time?":
            c = asctime()
            print("The time and date is", c)
            savefile()
            break
        if "sudo" in ask:
            c = "I'm afraid I can't do that."
            print("HAL says: I'm sorry " + ask + ", I'm afraid I can't do that.")
            savefile()
            break
        if ask == "What OS am I running?":
            c = platform()
            print("You are running ", c)                                                                                                                                                # Reports the system information (ex. Windows 8.1 shows up as "Windows-8-6.2.9200") and saves it.
            savefile()
            break
        if ask == "What can I say?":
            print("You can ask any question, though yes or no questions work better.")
            print("There are some hidden features too, such as:\n    Define (...)\n    What is the weather like?\n    What is the weather like in (...)\n    Start (application)")
            print("However, these features (excluding start) require an active internet connection.")
            break
        if ask == "What's the weather like?":
            print("Connecting to the internet and asking Google, please wait.")
            webopen('https://www.google.co.uk/?gws_rd=ssl#q=weather')
            print("Your web browser should now list the weather.")
            savefile()
            break
        if "What's the weather like in" in ask or "How do I say" in ask or "Define" in ask:
            print("Connecting to the internet and asking Google, please wait.")
            ask = ask.replace(" ", "+")
            webopen('https://www.google.co.uk/?gws_rd=ssl#q=' + ask)
            print("Your web browser should now list the info you require.")
            savefile()
            break
        if "Search" in ask:
            print("Connecting to the internet and asking Google, please wait.")
            ask = ask.replace(" ", "+")
            ask = ask.replace("Search", "")
            webopen('https://www.google.co.uk/?gws_rd=ssl#q=' + ask)
            print("Your web browser should now list the info you require.")
            savefile()
            break
        for x in range(1, 11):                                                                                                                                                          # For every number from 1 to 10:
            print("Shaking... \ ", end='\r'), sleep(0.05)																# Prints the message "Shaking" with a spinning cursor, replacing the text on each row.
            print("Shaking... | ", end='\r'), sleep(0.05)
            print("Shaking... / ", end='\r'), sleep(0.05)
            print("Shaking... - ", end='\r'), sleep(0.05)
            print(end='\r')
        c = choice([                                                                                                                                                                    # Chooses a result in the list randomly.
            "Try again later.",
            "Most certainly.",
            "The answer is something I cannot comprehend.",
            "java.lang.DoItLaterException(): Can't be bothered right now.",
            "No.",
            "Are you serious? No!",
            "Are you serious? Yes!",
            "Erm...okay. Sure.",
            "Yes.",
            "I don't know...",
            "Something tells me you shouldn't be asking me this...",
            "Quite possibly, though I cannot make any promises.",
            "Nah.",
            "Yeah!",
            "I fear GCHQ is watching, so I won't answer this.",
            "Haha, no.",
            "Hm, maybe.",
            "Okay, yeah. Why not?",
            "Google is your friend.",
            "Thinking about it, no.",
            "Thinking about it, yes.",
            "I'm probably not the person/bot you should be asking.",
            "Your parents might know.",
            "Look outside for more information.",
            "Consult the manual for more information.",
            "Check the enclosed instruction book.",
            "I don't know how to answer this. Try again when I can.",
            "Get back to me on that one, I need to think about it.",
            "Don't tell anyone, yes.",
            "Don't tell anyone, no.",
            "I'd like to direct you to Google.",
            "Try Googling it.",
            "Try Binging it.",
            "Try Yaho-actually, don't bother. Yahoo is awful.",
            "Ask Bill Nye, he's the science guy after all.",
        ])
        if ask == "Ping!":                                                                                                                                                              # Easter egg! If the user 'asks' "Ping!" it replies with "Pong!" and saves it.
            print("The Magic 8 Ball says: Pong!")
            c = "Pong!"
            savefile()
            break
        elif ask == "You're a wizard.":
            c = "I'm a WHAT?!"
            print("The Magic 8 Ball says:", c)
            savefile()
            break
        else:
            print("The Magic 8 Ball says:", c)                                                                                                                                          # The program replies with the result from the random choice above, and again uses the savefile() function to save the file.
            savefile()
            break
    quit1 = input("Would you like to restart? [Y/n] ")                                                                                                                                  # With any luck, all operations should eventually end up here.
    if quit1 == "n":
        break
print("\nThanks for playing! See you soon!")
sleep(2)
exit()
