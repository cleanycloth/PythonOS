from platform import system as syst
from os import system, path
from time import sleep
score = 0
name = ""
def savefile():
    game = open("testresults.txt", "a")
    game.write(name), game.write(": "), game.write(str(score)), game.write("\n"), game.close()
    sleep(2)
def question(qnum,question,answera,answerb,answerc,answerd,correct):
    global score
    print("\nQuestion " + str(qnum) + ": " + question)
    answer = input("A: " + answera + "\nB: " + answerb + "\nC: " + answerc + "\nD: " + answerd + "\n\nAnswer>")
    if answer.upper() == correct:
        print("Correct! That scores you a point.")
        score += 1
    else:
        print("Uh oh, that was incorrect. The correct answer was: " + correct + "\n")
def endoftest():
    print("That's the end of the test. See you next time!")
    print("You scored: " + str(score))
    sleep(2)
    print("Saving data, please wait.", end='\r')
    savefile()
    print("Data saved successfully! ")
    sleep(2.5)
    exit()
while 1:
    if syst() == 'Windows':
        system('cls')
    else:
        system('clear')
    print("Welcome to the Unit 1 Quiz!")
    name = input("Please enter your name: ")
    print("Ah, hello " + name + "! Let's get this party started.")
    question(1,"What is a paradigm?","A style or way of programming","A series of memory locations","A programming function","A sandwich","A")
    question(2,"What is a boolean?","A numeric value","True/False only","True/False and strings","A person that leans scarily","B")
    endoftest()
