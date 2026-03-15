class Restaurant:
    """Attempt to model a restraurant"""

    def __init__(self, restaurant_name, cuisine_type):
        """Initialize the restaurant name and cuisine type"""
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type

    def describe_restaurant(self):
        """Describes the restaurant"""
        print(f"{self.restaurant_name.title()} is a {self.cuisine_type} "
              "restaurant")

    def open_restaurant(self):
        """Indicates the restaurant is open"""
        print("The restaurant is open!")