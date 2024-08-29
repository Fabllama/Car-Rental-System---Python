class User:
    def __init__(self,user_id,name,phone,email,username,password,role,points):
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        self.points = points

    def check_password(self,username,password):
        return self.password == password

class User_List:
    def __init__(self):
        self.users = []

    def add_user(self,user):
        self.users.append(user)

    def auth_login(self,username,password):
        user = next((u for u in self.users if u.username == username), None)
        if user and user.check_password(password):
            return user
        return None

def login():
    username = input("Username : ")
    password = input("Password : ")
    User.check_password(username,password)

    if User:
        print("Welcome, "+{User.name}+"!")
        return User
    else:
        print("Invalid credentials")
        return None
    
def main():
    print("1. Login")
    print("2. Exit")
    print("3. Add User")
    choice = int(input("Enter your choice : "))

    if choice == 1:
        login()
    elif choice == 2:
        exit()
    elif choice == 3:
        username = input("New user : ")
        User_List.add_user(username)
    else:
        print("Invalid choice!")

#User_List.add_user(User(1,"alex",12345,"alex@gmail.com","alex1","password123","member",0))

if __name__ == "__main__":
    main()
    