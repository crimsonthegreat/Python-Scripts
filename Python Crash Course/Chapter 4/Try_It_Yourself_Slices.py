#List of Magicians
magicians = ['alice', 'kevin', 'david', 'keanu', 'obleck', 'ralph', 'george', 'antwon']
for magician in magicians:
    print(magician.title())
    print(f'{magician.title()}, that was a neat trick!')
    print(f"I can't wait to see your next trick {magician.title()}.\n")

print('Thank you everyone, for the great show.  We hope to see you again!')

#Print lines
print(f'The first 3 lines int the list are:\n{magicians[0:3]}')
print(f'Three items from the middle are:\n{magicians[2:5]}')
print(f'The last 3 lines are:\n{magicians[-3:]}')

#List of pizzas
pizzas = ['sausage', 'pepperoni', 'cheese']
friend_pizzas = pizzas[:]

#Append to list
pizzas.append('meats')
friend_pizzas.append('veggie')

#My favorite pizzas
print('My favorite pizzas are:')
for pizza in pizzas:
    print(pizza)

#Friends favorit pizzas
print('\nMy friends favorite pizzas are:')
for friend_pizza in friend_pizzas:
    print(friend_pizza)

print("\nI can't wait to have more pizza!")

#List of Foods
my_foods =['pizza', 'burgers', 'chicken']
friend_foods = my_foods[:]

my_foods.append('cheese cake')
friend_foods.append('ice cream')

print('\nMy favorite foods:')
for my_food in my_foods:
    print(my_food)

print('\nMy friends favorite food:')
for friend_food in friend_foods:
    print(friend_food)

