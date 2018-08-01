from time import sleep
from os import system
from platform import system as osdetect
from random import choice, randint
question = choice([
    "What would you like to do now?",
    "Alrighty, what's next?",
    "Anything else I can do?",
    "How else can I help?",
    "What else can I help you with?",
    "What can I do now?",
    "Hi!",
    "How can I help?",
    "What's on your mind?",
    ])
def clear():
    if osdetect() == "Windows":
        system('cls')
    else:
        system('clear')
def printquestion():
    if len(question) < 5:
        print(question.rjust(15))
    elif len(question) < 20:
        print(question.rjust(25))
    else:
        print(question.rjust(35))
def reset():
    sleep(0.1)
    clear()
    print("\n"*7)
def cortanaring():
    print("""
                *  *
             *        *
            *          *
            *          *
             *        * 
                *  *
    """)
def cortanaanimation():
    print("\n"*7)
    print("""\n\n
              **
              **
         """)
    reset()
    print("""\n\n
              * *
             *   *
              * *
        """)
    reset()
    print("""\n\n
               *  *
             *      *
            *        *
             *      *
               *  *
          """)
    reset()
    print("\n\n")
    cortanaring()

clear()
cortanaanimation()
sleep(0.5)
printquestion()
sleep(3)
clear()

for x in range(1,10):
    print("\n"*(9-int(x)))
    cortanaring()
    printquestion()
    sleep(0.02)
    clear()
cortanaring()
printquestion()
sleep(0.5)
clear()
cortanaring()
print("Here's some info for your evening."), sleep(0.03)
print("Current temperature: " + str(randint(5,25)) + "C - Mostly Clear (Precipitation: 0%)"), sleep(0.03)
print("-"*70), sleep(0.03)
print("Business News:"), sleep(0.03)
print("Donald Trump to FINALLY give up running for presidency"), sleep(0.03)
print("Microsoft shelling out billions for cat pictures to be placed\neverywhere on campus"), sleep(0.03)
print("Other boring news here"), sleep(0.03)
print("-"*70), sleep(0.03)
exit
