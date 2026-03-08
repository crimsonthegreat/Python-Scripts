def describe_pet(animal_type, pet_name):
    """Displays information about pet"""
    print(f"\nI have a {animal_type}")
    print(f"My {animal_type}'s name is {pet_name.title()}")

describe_pet('hamster', 'harry')
describe_pet('dog', 'rufus')
describe_pet(animal_type='hamster', pet_name='harry')
describe_pet(pet_name='harry', animal_type='hamster')

def describe_pet(pet_name, animal_type='dog'):
    """Displays information about pet"""
    print(f"\nI have a {animal_type}")
    print(f"My {animal_type}'s name is {pet_name.title()}")

describe_pet(pet_name='rufus')
describe_pet('rufus')
describe_pet(pet_name='harry', animal_type='hamster')
describe_pet('harry', 'hamster')