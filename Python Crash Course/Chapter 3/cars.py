#Initial list of cars
cars = ['bmw', 'audi', 'toyota', 'subaru']
#Sort cars int alphabetical order
cars.sort()
print(cars)

#Sort cars in reverse alphabetical order
cars.sort(reverse=True)
print(cars)

#Temporary sort of cars in alphabetical order
cars = ['bmw', 'audi', 'toyota', 'subaru']
print('\nOriginal order of the cars:')
print(cars)

print('\nHere is the sorted list of cars:')
print(sorted(cars))

print('\nOriginal order of the cars:')
print(cars)

#Reverse the order of the cars
print(f'\n {cars}')
cars.reverse()
print((cars))

#Find the length of the cars list
print(len(cars))