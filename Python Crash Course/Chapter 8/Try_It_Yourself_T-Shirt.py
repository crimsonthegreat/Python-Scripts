# 8.3
def make_shirt(size, message):
    """Make a T-Shirt"""
    print(f"\nThe T-Shirt size is {size}")
    print(f"The message on the shirt is: \n{message}")

message = "Sweet shirt!"
make_shirt('medium', message)
make_shirt(message=message, size='medium')

# 8.4
def make_shirt(size='large', message='I love Python'):
    """Make a T-Shirt"""
    print(f"\nThe T-Shirt size is {size}")
    print(f"The message on the shirt is: \n{message}")

make_shirt()
make_shirt('medium')
make_shirt(size='medium', message='Python is great')

# 8.5
def describe_city(city_name, country='the USA'):
    """Describes a city and the country it belongs to"""
    if country == 'the USA':
        country = 'the USA'
    else:
        country = country.title()

    print(f"\n{city_name.title()} is in {country}")

describe_city('Phoenix')
describe_city('munich', 'germany')
describe_city('sydney', 'australia')