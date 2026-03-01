#Intial list of Motorcycles
motorcycles = ['Honda', 'Yamaha', 'Suzuki']
print(motorcycles)

#Change the first motorcycle value
motorcycles[0] = 'Ducati'
print(f'\n{motorcycles}')

#Append Honda to the end of the list
motorcycles.append('Honda')
print(f'\n{motorcycles}')

#Empty list
motorcycles = []
#Append to list
motorcycles.append('Honda')
motorcycles.append('Yamaha')
motorcycles.append('Suzuki')
print(f'\n{motorcycles}')

#Insert a motorcycle into the list
motorcycles.insert(0, 'Ducati')
print(f'\n{motorcycles}')

#Delete a motorcycle from the list
del motorcycles[0]
print(f'\n{motorcycles}')

#Pop a motorcycle from the list
popped_motorcycle = motorcycles.pop()
print(f'\n{motorcycles}')
print(popped_motorcycle)
print(f'The last motorcycle I owned was a {popped_motorcycle}.')

#Pop any position in the list
motorcycles = ['Honda', 'Yamaha', 'Suzuki']
print(f'\n{motorcycles}')
first_owned = motorcycles.pop(0)
print(f'The first motorcycle I owned was a {first_owned}.title().')

#Remove a motorcycle by value
motorcycles = ['Honda', 'Yamaha', 'Suzuki', 'Ducati']
print(f'\n{motorcycles}')

motorcycles.remove('Ducati')
print(motorcycles)

#Remove a motorcycle by value with reason
motorcycles = ['Honda', 'Yamaha', 'Suzuki', 'Ducati']
print(f'\n{motorcycles}')

too_expensive = 'Ducati'
motorcycles.remove(too_expensive)
print(motorcycles)
print(f'A {too_expensive} is too expensive for me.')