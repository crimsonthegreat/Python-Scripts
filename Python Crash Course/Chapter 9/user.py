class User:
    """Model a user"""

    def __init__(self, first_name, last_name):
        """Initialize the user's first name and last name"""
        self.first_name = first_name
        self.last_name = last_name
        self.login_attempts = 0
        self.full_name = f"{first_name.title()} {last_name.title()}"
    
    def describe_user(self):
        """Describes a user"""
        print(f"{self.first_name.title()} {self.last_name.title()}")

    def greet_user(self):
        """Greet the user"""
        print(f"\nWelcome {self.first_name} {self.last_name}!")

    def increment_login_attempts(self):
        """Increments login attempts"""
        self.login_attempts += 1

    def reset_login_attempts(self):
        """Reset login attempts to 0"""
        self.login_attempts = 0

