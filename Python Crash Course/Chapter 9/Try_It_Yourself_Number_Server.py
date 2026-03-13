# 9.4
class Restaurant:
    """Attempt to model a restraurant"""

    def __init__(self, restaurant_name, cuisine_type):
        """Initialize the restaurant name and cuisine type"""
        self.restaurant_name = restaurant_name
        self.cuisin_type = cuisine_type
        self.number_served = 0

    def describe_restaurant(self):
        """Describes the restaurant"""
        print(self.restaurant_name)
        print(self.cuisin_type)

    def open_restaurant(self):
        """Indicates the restaurant is open"""
        print("The restaurant is open!")
    
    def set_number_served(self, served):
        """Set the number of servered guests"""
        if served >= self.number_served:
            self.number_served = served
        else:
            print("You cannot server less customers!")
    
    def increment_number_served(self, serve):
        """Increment the number of customers served"""
        self.number_served +=  serve

restaraunt = Restaurant("jacki chan's", "chinese")
print(f"{restaraunt.restaurant_name.title()}, "
      f"a {restaraunt.cuisin_type.title()} restaraunt, "
      f"has servered {restaraunt.number_served} customers")

restaraunt.number_served = 200
print(f"{restaraunt.restaurant_name.title()}, "
      f"a {restaraunt.cuisin_type.title()} restaraunt, "
      f"has servered {restaraunt.number_served} customers")

restaraunt.set_number_served(500)
print(f"{restaraunt.restaurant_name.title()}, "
      f"a {restaraunt.cuisin_type.title()} restaraunt, "
      f"has servered {restaraunt.number_served} customers")

restaraunt.increment_number_served(3000)
print(f"{restaraunt.restaurant_name.title()}, "
      f"a {restaraunt.cuisin_type.title()} restaraunt, "
      f"has servered {restaraunt.number_served} customers")

# 9.5
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
        print(f"{self.first_name} {self.last_name}")

    def greet_user(self):
        """Greet the user"""
        print(f"\nWelcome {self.first_name} {self.last_name}!")

    def increment_login_attempts(self):
        """Increments login attempts"""
        self.login_attempts += 1

    def reset_login_attempts(self):
        """Reset login attempts to 0"""
        self.login_attempts = 0

user = User("joe", "blow")
while user.login_attempts < 6:
    print(f"{user.full_name} has attempted to login {user.login_attempts} "
          "times")
    user.increment_login_attempts()

user.reset_login_attempts()
print(f"{user.full_name} has attempted to login {user.login_attempts} "
      "times")
