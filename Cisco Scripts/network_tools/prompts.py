def user_input(prompt):
    """User prompts to continue"""
    
    while True:
        user_input = input(prompt).lower().strip()

        if user_input in ("n", "no"):
            quit()
        elif user_input in ("y","yes"):
            break
        elif user_input == "q":
            quit()
        else:
            print("Please enter y or n to continue!")