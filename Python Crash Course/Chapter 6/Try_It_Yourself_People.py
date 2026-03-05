muchow = {'first_name' : 'john', 'last_name' : 'muchow', 'age' : 45, 'city' : 'springfield'}
reddog = {'first_name' : 'bob', 'last_name' : 'the builder', 'age' : 57, 'city' : 'canloops'}
hammerhead = {'first_name' : 'mark', 'last_name' : 'gresko', 'age' : 60, 'city' : 'phoenix'}

people = [muchow, reddog, hammerhead]

for person in people:
    print(person)

maximus = {'animal' : 'dog', 'owner' : 'jim bob'}
callie = {'animal' : 'cat', 'owner' : 'jake'}
lexie = {'animal' : 'hamster', 'owner' : 'jessie'}

pets = [maximus, callie, lexie]

for pet in pets:
    print(pet)

favorite_places = {
    'muchow' : 'nature',
    'reddog' : 'a construction site',
    'goose' : 'the ocean',
}

for person, place in favorite_places.items():
    print(f"{person}'s favorite place to go is {place}")

favorite_numbers = {
    'sally' : [2, 10],
    'joe' : [12],
    'jim' : [65, 82, 15],
}

for person, numbers in favorite_numbers.items():
    print(f"{person}'s favorite number is:")
    for number in numbers:
        print(f'\t{number}')

cities = {
    'phoenix' : {
        'population' : 'way to many',
        'country' : 'usa',
        'fact' : 'really hot',
    },
    'munich' : {
        'population' : '1604384',
        'country' : 'germany',
        'fact' : 'great beer',
    },
    'tokyo' : {
        'population' : '14000000',
        'country' : 'japan',
        'fact' : 'land of the rising sun',
    },
}

for city, info in cities.items():
    print(city)
    print(f"\t{info['population']}\n\t{info['country']}"
          f"\n\t{info['fact']}")