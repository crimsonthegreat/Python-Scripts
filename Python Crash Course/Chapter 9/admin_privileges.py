from user import User

class Privileges:
    """Model user privileges"""

    def __init__(self):
        """"Initialize privilges"""
        self.privileges = [
                           'can add post',
                           'can can delete post', 
                           'can ban user'
                          ]
        
    def show_privileges(self):
        """Print admin privileges"""
        print("\nThe admin user has the following admin privileges:")
        for privilege in self.privileges:
            print(privilege)

class Admin(User):
    """Model and admin user"""

    def __init__(self, first_name, last_name):
        """Inheret from parent class User"""
        super().__init__(first_name, last_name)
        self.privileges = Privileges()