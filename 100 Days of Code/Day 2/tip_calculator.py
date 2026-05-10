def break_loop(user_input):
    if user_input == 'q' or user_input == 'Q':
        quit()
    else:
        pass

def user_input(message):
    while True:
        user_input = input(message)
        break_loop(user_input)

        try:
            user_input = int(user_input)
            break
        except ValueError:
            print("Please enter a number!")
    return user_input

print("Welcome to the tip calculator!")
print("You may enter q at any time to quit...")

while True:
    bill_msg = "What was the total bill?\n"
    bill = user_input(bill_msg)

    print(f"The total bill is ${bill}")

    tip_msg = "How much would you like to tip?\n"
    tip = user_input(tip_msg)

    bill *= ((tip * .01) + 1)
    print(f"The total bill with a {tip}% is {bill}")

    num_people_msg = "How many people should the bill be split between?\n"
    num_people = user_input(num_people_msg)

    bill /= num_people
    print(f"The bill per person when split between {num_people} is {bill}")  

    while True:
        cont = input("Would you like to calculate another bill? [y/n]:\n")

        if cont == 'y' or cont == 'Y':
            break
        elif cont == 'n' or cont == 'N':
            quit()
        else:
            print("Please answer with a y or n...")