# 9.6
class Restaurant:
    """Attempt to model a restraurant"""

    def __init__(self, restaurant_name, cuisine_type):
        """Initialize the restaurant name and cuisine type"""
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type

    def describe_restaurant(self):
        """Describes the restaurant"""
        print(self.restaurant_name)
        print(self.cuisine_type)

    def open_restaurant(self):
        """Indicates the restaurant is open"""
        print("The restaurant is open!")

class IceCreamStand(Restaurant):
    """Attempt to model an ice cream stand"""
    
    def __init__(self, restaraunt_name, cuisine_type):
        """Initialize attributes from class Restaraunts"""
        super().__init__(restaraunt_name, cuisine_type)
        self.flavors = ['vanilla', 'chocolate', 'mint chip']

    def list_flavors(self):
        """Print the list of flavors"""
        print("\nHere are today's flavors:")
        for flavor in self.flavors:
            print(flavor)

icecream = IceCreamStand("brain freeze", "ice cream")
icecream.list_flavors()

# 9.7
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

class Admin(User):
    """Model and admin user"""

    def __init__(self, first_name, last_name):
        """Inheret from parent class User"""
        super().__init__(first_name, last_name)
        self.privileges = [
                           'can add post',
                           'can can delete post', 
                           'can ban user'
                          ]
    
    def show_privileges(self):
        """Print admin privileges"""
        print("\nThis user has the following admin privileges:")
        for privilege in self.privileges:
            print(privilege)

admin = Admin('joe', 'blow')
admin.show_privileges()

# 9.8
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
        print("\nThis user has the following admin privileges:")
        for privilege in self.privileges:
            print(privilege)

class Admin(User):
    """Model and admin user"""

    def __init__(self, first_name, last_name):
        """Inheret from parent class User"""
        super().__init__(first_name, last_name)
        self.privileges = Privileges()
    
admin = Admin('joe', 'blow')
admin.privileges.show_privileges()

# 9.9
class Car:
    """A simple attempt to represent a car"""
    
    def __init__(self, make, model, year):
        """Initialize the make, model, and year of a car"""
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def get_descriptive_name(self):
        """Return a neatly formatted descriptive name."""
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()
    
    def read_odometer(self):
        """Print a statement showing the car's mileage"""
        print(f"This car has {self.odometer_reading} miles on it")

    def update_odometer(self, mileage):
        """
        Set the odometer reading to the given value.
        Reject the change if it attempts to roll the odometer back.
        """
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't roll back an odometer!")


    def increment_odometer(self, miles):
        """Add the given amount to the odometer reading"""
        self.odometer_reading += miles

class Battery:
    """A simple attempt to model a battery for an electric car"""

    def __init__(self, battery_size=40):
        """Initialize the battery's attributes."""
        self.battery_size = battery_size
    
    def describe_battery(self):
        """Print a steatment describing the battery size"""
        print(f"\nThis car has a {self.battery_size}-KWH battery.")
    
    def get_range(self):
        """Print a statementabout the range this battery provides."""
        if self.battery_size == 40:
            range = 150
        elif self.battery_size == 65:
            range = 225

        print(f"This car can go about {range} mailes on a full charge.")

    def upgrade_battery(self):
        """Upgrade the battery on an electric car"""
        print("\nYou electric car is getting a battery upgrade!")
        if self.battery_size == 40:
            self.battery_size = 65


class ElectricCar(Car):
    """Represents aspects of a car, specific to electric vehicles"""

    def  __init__(self, make, model, year):
        """
        Initialize attributes from parent class. 
        Then initialize attributes specific to an electric car.
        """
        super().__init__(make, model, year)
        self.battery = Battery()

my_leaf = ElectricCar('nissan', 'leaf', 2024)
my_leaf.battery.describe_battery()
my_leaf.battery.get_range()
my_leaf.battery.upgrade_battery()
my_leaf.battery.describe_battery()
my_leaf.battery.get_range()