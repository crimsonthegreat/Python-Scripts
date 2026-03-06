# 7.1
rental_car = input("Please tell me what kind of car you would like to rent? ")
print(f"I will try to see if we have a {rental_car}")

# 7.2
dinner_group = input("Can you please let me know how many will be dinning with us tonight? ")
dinner_group = int(dinner_group)

if dinner_group > 8:
    print("Your wait will be 15 minutes.")
else:
    print("We can seat you now.")

#7.3
multiples = input("Please enter a number: ")
multiples = int(multiples)

if multiples % 10 == 0:
    print("This is a multiple of 10")
else:
    print("This is not a multiple of 10")