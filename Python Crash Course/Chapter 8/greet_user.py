def greet_user(names):
    """Print a simple message to great user in the list"""
    for name in names:
        msg = f"Hello, {name.title()}"
        print(msg)

username = ['hannah', 'ty', 'margot']
greet_user(username)