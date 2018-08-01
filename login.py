def login():
    from getpass import getpass
    from os import path
    def password():
        passw = getpass(prompt='Password: ')
        passw1 = open('Users/' + user1, "r")
        if not passw in passw1:
            print("Invalid password.")
        else:
            print("\nLogged in as " + user + ".\n")
            file = open('currentuser.txt', "w")
            file.write(user1), file.close()
    while 1:
        user = input("login> ")
        if path.exists("Users/" + user + ".limited") or path.exists("Users/" + user + ".admin"):
            if user.lower() == "public":
                print("\nLogged in as " + user.lower() + ".\n")
                user = user + ".limited"
                file = open('currentuser.txt', "w")
                file.write(user), file.close()
                return True
            user1 = user + ".limited"
            if path.exists("Users/" + user1):
                password()
                return True
            else:
                user1 = user + ".admin"
                password()
                return True
        else:
            print("Invalid username, or the user has not been created.")
