# 7.4 Pizza Toppings
prompt = "\nPlease enter the toppings you would like on your pizza:"
prompt += "\n(Enter 'quit' when you have finished). "

toppings = ""
while toppings != 'quit':
    toppings = input(prompt)

    if toppings != 'quit':
        print(f"Adding {toppings} to the pizza.")

# 7.5 Movie Tickets
prompt = "\nPlease enter your age:"
prompt += "\n(Enter 'quit' when you are finished). "

active = True
while active:
    age = input(prompt)

    if age == 'quit':
        active = False
    else:
        age = int(age)

        if age < 3:
            print("Your ticket is free!")
        elif age < 12:
            print("Your ticket is $10.")
        else:
            print("Your ticket is $15")