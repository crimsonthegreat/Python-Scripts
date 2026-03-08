# 8.12
def build_sandwiches(*toppings):
    """Print the toppings wanted for a sandwich"""
    print("\nThe sandwich will have the following toppings:")
    for topping in toppings:
        print(topping)

build_sandwiches('ham')
build_sandwiches('ham', 'cheddar cheese')
build_sandwiches('salami', 'pepperoni', 'ham', 'pepper jack cheese')

# 8.13
def build_user_profile(f_name, l_name, **user_info):
    """Display user info for selected user"""
    user_info['first_name'] = f_name
    user_info['last_name'] = l_name
    return user_info

user_profile = build_user_profile('crimson', 'thegreat', 
                                  location='phoenix', job='network engineer',
                                  why_python='ccie')

print(user_profile)

# 8.14
def build_car(manufacturer, model, **car_info):
    """Displays information about a car"""
    car_info['manufacturer'] = manufacturer
    car_info['model'] = model
    return car_info

car_facts = build_car('Jeep', 'Wrangler', color='orange', tow_package=True)
print(car_facts)