# Arbitrary arguements
def make_pizza(*toppings):
    """Summeraize the pizza we are about to make"""
    print("\nMaking a pizza with the following toppings:")
    for topping in toppings:
        print(topping)

make_pizza('pepperoni')
make_pizza('pepperoni', 'jalapano', 'sausage')

# Mixing positional and arbitrary arguements
def make_pizza(size, *toppings):
    """Summeraize the pizza we are about to make"""
    print(f"\nMaking a {size}-inch pizza with the following toppings:")
    for topping in toppings:
        print(topping)

make_pizza(16, 'pepperoni')
make_pizza(20, 'pepperoni', 'ham', 'sausage')