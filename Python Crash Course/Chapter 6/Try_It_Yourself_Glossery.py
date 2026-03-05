glossery = {
    'variable' : 'container for storing data',
     'list' : 'mutable and ordered data structure used to store a collection of items',
     'tuple' : 'immutable and ordered data structure used to store a collection of items',
     'dictionary' : 'key value pairs',
     'for loop' : 'control flow statement used to iterate over a sequence',
     'if' : 'conditional control flow statement that executes a block of code only if a specified condition evaluates to true',
     'elif' : 'check multiple conditions sequentially when preceeding if or elif is false',
     'else' : 'specifies a block of code to be executed when a certain condition is false in control flow statements',
     'set' : 'a collection  in which each item must be unique',
     'append' : 'add items to a list or tuple',
     }

for gloss, term in glossery.items():
    print(f'{gloss}:\n\t{term}')

rivers = {'nile' : 'egypt', 'mississippi' : 'mississippi', 'colorado' : 'arizona'}

for river, place in rivers.items():
    print(f'The {river.title()} river runs through {place.title()}')

for river in rivers.keys():
    print(river.title())

for place in rivers.values():
    print(place.title())

favorite_language = {
    'jen' : 'python',
    'sarah' : 'c',
    'edward' : 'rust',
    'phil' : 'python',
    }

take_poll = ['jen', 'jake', 'sue', 'sarah', 'john']

for pollee in take_poll:
    if pollee not in favorite_language.keys():
        print(f'{pollee.title()} would you like to take our poll?')
    else:
        print(f'{pollee.title()} thank you for taking our poll!')