# A level Authentication Challenge

class UserStore():
    username = None
    validated = False
#end class

class User():	
    username = ""
    password = ""
    first_name = ""
    surname = ""
#end class

users = []	

def encrypt_ceasar(password, key): #assumption - only lower case a-z
    lowest_char_num = ord("a") # would be ok to hard code this (97)

    temp_password = ""
    for c in password:
            
        # all the following uncommented lines can be combined into just this 
        # one line below ! I have split it for easier understanding.
        # temp_password += chr((ord(c) + key - lowest_char_num) % 26 + lowest_char_num)
        
        new_char_num = ord(c)
        new_char_num += key
        zero_bound_char = new_char_num - lowest_char_num
        new_char_num = (zero_bound_char % 26) + lowest_char_num
        new_char = chr(new_char_num)
        temp_password += new_char
    #next c
    return(temp_password)
#end def

def get_users():
    raw_data = None
    user_data = []
    try:
        with open("users.txt", "r") as f:
            raw_data = f.readlines()
        #end with
    except:
        print("Error loading data")
        return None
    #end try	
    
    for line in raw_data:
        #strip the \n from the end
        stripped_line = line.strip()
        #get the array of details for each user and create a dictionary !!
        sep_data = stripped_line.split(",")
        
        #we should have 4 fields
        if len(sep_data) == 4:
            user = User()
            user.username = sep_data[0]
            user.password = sep_data[1]
            user.first_name = sep_data[2]
            user.surname = sep_data[3]
            user_data.append(user)
        else:
            print("Error loading data")
            return None
        #end if
    #next line	
    return user_data
#end def

def get_user_index(username):
    for index, user in enumerate(users):
        if user.username.lower() == username.lower():
            return index
        #end if
    #next index
    return -1	
#end def

def get_user(username):
    for user in users:
        if user.username.lower() == username.lower():
            return user
        #end if
    #next index
    return None	
#end def

def login():
    global users
    
    username = input("Enter your user name: ")
    password = input("Enter your password: ")
            
    # The password should be decrypted, key = 3
    encrypted_password = encrypt_ceasar(password, 3)
    
    # first lets get the users
    users = get_users()
    if users == None: 
        print("Error getting data")
        return
    #end if
    
    user = get_user(username)
    
    if user is not None and user.password == encrypted_password:
        print("Welcome,", user.first_name, user.surname)
        UserStore.username = username
        UserStore.validated = True
        user_found = True
    else:
        print("You have entered incorrect credentials")
        UserStore.username = ""
        UserStore.validated = False			
    #end if
#end def

def print_user_details(username):
	
    user = get_user(username)
    if user is None: return
    print()
    print("Details:")
    print("Username: " + user.username)
    print("First name: " + user.first_name)
    print("Surname: " + user.surname)
    
    print()
#end def

def view_details():
    if UserStore.username == None or not UserStore.validated:
        print("You need to log in first\n")
        return
    #end if
    username = UserStore.username
    print_user_details(username)
#end def

def dict_to_cs_string(user):
    return user.username + "," + user.password + "," + user.first_name + "," + user.surname
#end if

def save_users():
    try:
        with open("users.txt", "w") as f:
            for user in users:
                line = dict_to_cs_string(user)
                f.write(line + "\n")
            #next user
        #end with
    except:
        print("Error saving data")
    #end try		
#end def

def change_password():
    global users
    username = ""
    try:
        username = UserStore.username
        if username == None or not UserStore.validated:
            print("You need to log in first\n")
            return
        #end if
    except: # most likely no key found
        print("You need to log in first\n")
        return
    is_updated = False
    while not is_updated:
        new_password = input("Enter password: ")
        new_password_check  = input("Enter new password again: ")
        
        if new_password != new_password_check:
            print("Your passwords don't match")
            continue                     
        #end if
        
        new_password = encrypt_ceasar(new_password,3)
        user_index = get_user_index(username)
        users[user_index].password = new_password
        save_users()
        is_updated = True
    #end while
#end def

def menu():
    print("Welcome to the authentication program")
    print("1. Login")
    print("2. Change Password")
    print("3. View my details")
    print("4. Quit")

    choice = input("Enter your choice: ")
    return choice	
#end def


def main():

    choice = ""
    while choice != "4":
        choice = menu()
        
        if choice == "1":
            login()
        elif choice == "2":
            change_password()
        elif choice == "3":
            view_details()
        else:
            print("\nSelect a valid choice\n")
        #end if	
    #end while	
    print("Goodbye")
#end def
	

if __name__ == "__main__":
    main()
#end if
	
	



	
