from pathlib import Path
import json

# 10.13 create dictionary for user and add additional user data
# build off of remember_me.py
def get_stored_username(path):
    """Get stored username if available"""
    if path.exists():
        contents = path.read_text()
        user_info = json.loads(contents)
        return user_info
    else:
        return None

def get_new_username(path):
    """Prompt for a new username"""
    username = input("What is your name? ")
    user_favorite_number = input("What is your favorite number? ")
    user_favorite_food = input("What is your favorite food? ")
    user_info = {
        'username' : username,
        'favorite number' : user_favorite_number,
        'favorite food' : user_favorite_food
    }
    contents = json.dumps(user_info)
    path.write_text(contents)
    return user_info
        
def greet_user():
    """Greet the user by name"""
    path = Path('username.json')
    user_info = get_stored_username(path)
    print(f"Are you {user_info['username'].title()}? (y/n)")
    while True:
        same_user = input().lower()
        if same_user == 'y':
            print(f"Welcome back, {user_info['username'].title()}!")
            print(f"I remember your favorite number is "
                  f"{user_info['favorite number']}.")
            print(f"I also remember your favorite food is "
                  f"{user_info['favorite food'].title()}")
            break
        elif same_user == 'n':
            user_info = get_new_username(path)
            print(f"We'll remember you when you come back, "
                  f"{user_info['username'].title()}!")
            print(f"Your favorite number {user_info['favorite number']}"
                  " will also be remembered!")
            print(f"We also will not forget your favorite food is "
                  f"{user_info['favorite food'].title()}")
            break
        else:
            print("Please enter y or n only")       

greet_user()