option = ""
number = ""
while 1:
    option = input("Select an option:\n1: Denary to Hex\n2: Denary to Bin\n3: Hex to Denary\n4: Bin to Denary\nq: Exit\n>>")
    if option == "1":
        while 1:
            try:
                number = input("Denary to Hex. Type q to return: ")
                if number == "q":
                    break
                print(hex(int(number)))
            except:
                print("That didn't work. Try again.")
    
    elif option == "2":
        while 1:
            try:
                number = input("Denary to Binary. Type q to return: ")
                if number == "q":
                    break
                print(bin(int(number)))
            except:
                print("That didn't work. Try again.")
    elif option == "3":
        while 1:
            try:
                number = input("Hex to Denary. Type q to return: ")
                if number == "q":
                    break
                print(str(int(number,16)))
            except:
                print("That didn't work. Try again.")
    elif option == "4":
        while 1:
            try:
                number = input("Binary to Denary. Type q to return: ")
                if number == "q":
                    break
                print(str(int(number,2)))
            except:
                print("That didn't work. Try again.")
    elif option == "q":
        exit()
    else:
        print("That didn't work. Try again.")
