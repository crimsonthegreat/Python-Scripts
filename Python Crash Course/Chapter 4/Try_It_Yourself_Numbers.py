for number in range(1, 21):
    print(number)

one_million = []
for value in range(1, 1000001):
    one_million.append(value)

print(f'{one_million}\n')
print(f'{max(one_million)}\n')
print(f'{min(one_million)}\n')
print(f'{sum(one_million)}\n')


odds = []
for odd in range(1, 21, 2):
    odds.append(odd)

print(f'{odds}\n')

threes = []
for three in range(1, 31):
    threes.append(three)

print(f'{threes}\n')

cubes = []
for cube in range (1, 11):
    cubes.append(cube)

print(f'{cubes}\n')

cubes = [num**3 for num in range(1, 11)]
print(cubes)