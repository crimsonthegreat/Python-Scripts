muchow = {'first_name' : 'john', 'last_name' : 'muchow', 'age' : 45, 'city' : 'springfield'}
print(muchow)

people_numbers = {'reddog' : 0, 'muchow' : 34, 'hammerhead' : 200, 'goose' : 150, 'slick' : 1888}

for person in people_numbers:
    print(f"{person}'s favorite number is {people_numbers[person]}")

glossery = {
    'variable' : 'container for storing data',
     'list' : 'mutable and ordered data structure used to store a collection of items',
     'tuple' : 'immutable and ordered data structure used to store a collection of items',
     'dictionary' : 'key value pairs',
     'for loop' : 'control flow statement used to iterate over a sequence'
     }

for gloss in glossery:
    print(f'{gloss}:\n\t{glossery[gloss]}')