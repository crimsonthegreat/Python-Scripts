# Function to quit the loop
def break_loop(user_input):
    if user_input == 'q' or user_input == 'Q':
        quit()
    else:
        pass

print("Band Name Generator")

# While Loop for generating a Band Name based on place of birth and favorite pet
while True:
    print("Let's generate a band name for you!")
    print("Type q at any time to exit...")

    # Get user input for place of birth
    born = input("Where were you born: ")

    # Check if the user wants to quit by checking for q or Q
    break_loop(born)

    # Get user input on favorite pet
    pet = input("What was your favor pet growing up: ")

    # Check if the user wants to quit by checking for q or Q
    break_loop(pet)

    # Output recommend band name
    print("Recommended band name:")
    print(f"{born} {pet}")

    # While Loop to see if the users wants to generate additional band name
    while True:
        leave = input("Would you like to generate another name: y or n: ")

        if leave == 'y' or leave == 'Y':
            break
        elif leave == 'n' or leave == 'N':
            quit()
        else:
            print("Please enter y or n...")