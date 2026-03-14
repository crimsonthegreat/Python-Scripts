# 9.1
class Restaurant:
    """Attempt to model a restraurant"""

    def __init__(self, restaurant_name, cuisine_type):
        """Initialize the restaurant name and cuisine type"""
        self.restaurant_name = restaurant_name
        self.cuisin_type = cuisine_type

    def describe_restaurant(self):
        """Describes the restaurant"""
        print(self.restaurant_name)
        print(self.cuisin_type)

    def open_restaurant(self):
        """Indicates the restaurant is open"""
        print("The restaurant is open!")

restaurant = Restaurant("Jackie Chan's", "Chinese")
print(f"\nThe restaurant's name is {restaurant.restaurant_name}.")
print(f"It serves {restaurant.cuisin_type} food!")
restaurant.describe_restaurant()
restaurant.open_restaurant()

# 9.2

my_restaurant = Restaurant('Schnitzel Haus', 'German')
your_restaurant = Restaurant('Screaming Eagles', 'American')
their_restaurant = Restaurant('Sluggish', 'French')

my_restaurant.describe_restaurant()
your_restaurant.describe_restaurant()
their_restaurant.describe_restaurant()

# 9.3
class User:
    """Model a user"""

    def __init__(self, first_name, last_name):
        """Initialize the user's first name and last name"""
        self.first_name = first_name
        self.last_name = last_name
    
    def describe_user(self):
        """Describes a user"""
        print(f"{self.first_name} {self.last_name}")

    def greet_user(self):
        """Greet the user"""
        print(f"\nWelcome {self.first_name} {self.last_name}!")

user1 = User('Todd', 'Howard')
user2 = User('Eric', 'Nylund')
user3 = User('Marty', "O'Donnell")

user1.greet_user()
user2.greet_user()
user3.greet_user()

