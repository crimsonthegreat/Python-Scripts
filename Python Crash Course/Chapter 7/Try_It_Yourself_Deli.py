# 7.8
sandwich_orders = ['ruben', 'italian', 'ham', 'turkey', 'meatball']
finished_sandwiches = []

while sandwich_orders:
    current_sandwich = sandwich_orders.pop()

    print(f"\nI made your {current_sandwich} sandwich.")
    finished_sandwiches.append(current_sandwich)

print("\nSandwiches that have been made:")
for sandwich in finished_sandwiches:
    print(sandwich)

# 7.9
sandwich_orders = ['ruben', 'pastrami', 'italian', 'ham', 'pastrami', 'turkey', 'meatball', 'pastrami']
finished_sandwiches = []
print("\nThe deli has run out of pastrami.")

while 'pastrami' in sandwich_orders:
    sandwich_orders.remove('pastrami')

print("\nHere are the remaining orders")
for sandwich in sandwich_orders:
    print(sandwich)

# 7.10
dream_vacation = {}

vacation_active = True
while vacation_active:
    name = input("\nWhat is your name: ")
    vacation = input("What is your dream vacation: ")

    dream_vacation[name] = vacation

    
    repeat = input("\nWould you like to let someone else answer about their dream vacation? (yes/no)")
    if repeat == 'no':
        vacation_active = False

print("\n--- Polling Results ---")
for name, vacation in dream_vacation.items():
    print(f"{name.title()} has a dream of going on vacation to {vacation}")