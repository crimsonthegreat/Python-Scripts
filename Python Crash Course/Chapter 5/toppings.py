requested_topping = 'mushrooms'

if requested_topping != 'Anchovies':
    print('Hold the anchovies!\n')

requested_toppings = ['mushrooms', 'extra cheese']

if 'mushrooms' in requested_toppings:
    print('Adding mushrooms')
if 'pepperoni' in requested_toppings:
    print('Adding pepperoni')
if 'extra cheese' in requested_toppings:
    print('Adding extra cheese')

print('\nFinished making your pizza\n')

requested_toppings = ['mushrooms', 'extra cheese', 'green peppers']

for topping in requested_toppings:
    print(f'Adding {topping}')

print('\nFinished making your pizza\n')

for topping in requested_toppings:
    if 'green peppers' in topping:
        print(f'We are out of {topping}')
    else:
        print(f'Adding {topping}')

print('\nFinished making your pizza\n')

requested_toppings = []

if requested_toppings:
    for requested_topping in requested_toppings:
        print(f'Adding {topping}')
    print('\nFinished making your pizza\n')
else:
    print('Are you sure you want a plain pizza?\n')

available_toppings = ['pepperoni', 'extra cheese', 'sausage', 
                      'green peppers', 'mushrooms', 'olives']

requested_toppings = ['mushrooms', 'french fries', 'extra cheese']

if requested_toppings:
    for requested_topping in requested_toppings:
        if requested_topping in available_toppings:
            print(f'Adding {requested_topping}')
        else:
            print(f'{requested_topping} is not available')
    print('\nFinished making your pizza\n')
else:
    print('Are you sure you want a plain pizza?')