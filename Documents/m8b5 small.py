#!/usr/bin/python
# The Magic 8 Ball, programmed by Aidan Rayner with optimization and some extra features by Nathan Barrall (choice feature).
from random import choice                                                                       # Imports random from choice
from platform import system as syst
from os import system, path
from time import sleep                                                                          # Imports asctime and sleep from time
def savefile():                                                                                 # Creates a function (savefile()) with the code attached to it listed below
        game = open("m8ballresults.txt", "a")                                                   # Opens results file for editing
        game.write(start), game.write("\n"), game.write(ask), game.write("\n"), game.write(c), game.write("\n\n"), game.close(), print("\nYour data has been saved.")
        sleep(1)                                                                                # Waits for one second
while 1:                                                                                        # Initiates an infinite loop, until broken.
    c = ""
    if syst() == 'Windows':                                                                     # Checks if the operating system is Windows. If it is, it runs the 'cls' command. If not, it runs the 'clear' command. This clears the screen.
        system('cls')
    else:
        system('clear')
    print("Magic 8 Ball Slim V1".rjust(79))
    if not path.exists("m8ballresults.txt"):                                                    # Checks for the results file
        file = open('m8ballresults.txt', "w"), file.close()                                     # Creates new results file if not found by opening a new file, then closing it.
        print("New results file generated.")
    if not path.exists("m8ballusernames.txt"):                                                  # Checks for the usernames file
        file2 = open('m8ballusernames.txt', "w"), file2.close()
        print("New usernames file generated.")                                                  # If not found, it generates a new one.
    print(), print("Hello! Welcome to Magic 8 Ball - Python Edition!")
    start = input("What is your name? : ")                                                      # Asks for your name
    if start in open('m8ballusernames.txt').read():                                             # Checks if the current user has logged in before. If they have, the program prints the next line and continues.
        print("Welcome back! I see you seek more advice.")
    else:
        qu = input("Thank you for signing in for the first time.\nYour name, question, and answer will be saved to a file in plaintext. \nDo you accept? [y/N] ")# Asks the user if they want to store their name in plaintext. This is required to use the program.
        if qu == "y":
            file3 = open('m8ballusernames.txt', "a")
            file3.write(start), file3.write(", "), file3.close()                                # Saves the username to a file
            print("Thank you. Your username has been saved.")
        else:
            print("You have not accepted the EULA. Magic 8 Ball cannot continue.")
            break
    ask = input("\nAsk me a question! Any question; I don't mind. : ")                          # Asks the user for a question.
    print()
    for x in range(1, 11):                                                                      # For every number from 1 to 10:
        print("Shaking... \ ", end='\r'), sleep(0.05)					        # Prints the message "Shaking" with a spinning cursor, replacing the text on each row.
        print("Shaking... | ", end='\r'), sleep(0.05)
        print("Shaking... / ", end='\r'), sleep(0.05)
        print("Shaking... - ", end='\r'), sleep(0.05)
        print(end='\r')
    c = choice([                                                                                # Chooses a result in the list randomly.
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
    print("The Magic 8 Ball says:", c)                                                          # The program replies with the result from the random choice above, and again uses the savefile() function to save the file.
    savefile()
    quit1 = input("Would you like to restart? [Y/n] ")                                          # With any luck, all operations should eventually end up here.
    if quit1.lower() == "n":
        break
print("\nThanks for playing! See you soon!")
sleep(2)
exit()
