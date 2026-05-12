import random

def rps():
    while True:
        print("Welcome to Rock, Paper, Scissors!")
        print("Choose your object: ")
        print("    Type: Rock, Paper, or Scissors")

        user_input = input("[Rock, Paper, Scissors]\n")
        user_input = user_input.title()

        if user_input == 'Rock':
            print("You chose Rock")
            rock()
        elif user_input == 'Paper':
            print("You chose Paper")
            paper()
        elif user_input == 'Scissors':
            print("You chose Scissors")
            scissors()
        else:
            print("Please enter Rock, Paper, or Scissors")

        comp_choice = random_choice()

        evaluation(user_input, comp_choice)
        quit_game()
        

def quit_game():
    while True:
            print("Would you like to play again?")

            user_input = input("[y/n]\n")
            user_input = user_input.title()

            if user_input == 'Y':
                break
            elif user_input == 'N':
                quit()
            else:
                print("Please enter y or n")

def random_choice():
    random_rps = random.randint(1, 3)

    if random_rps == 1:
        comp_choice = 'Rock'
        print(f"The computer chose {comp_choice}")
        rock()
    elif random_rps == 2:
        comp_choice = 'Paper'
        print(f"The computer chose {comp_choice}")
        paper()
    elif random_rps == 3:
        comp_choice = 'Scissors'
        print(f"The computer chose {comp_choice}")
        scissors()

    return comp_choice

def evaluation(user_input, comp_choice):
        if user_input == comp_choice:
            print('It was a draw')
        elif user_input == 'Rock' and comp_choice == 'Paper' \
            or user_input == 'Paper' and comp_choice == 'Scissors' \
                or user_input == 'Scissors' and comp_choice == 'Rock':
            print("You Lose!")
        else:
            print("You win!")

def rock():
    print("""
            _______
        ---'   ____)
              (_____)
              (_____)
              (____)
        ---.__(___)
        """)

def paper():
    print("""
            _______
        ---'    ____)____
                   ______)
                   _______)
                  _______)
        ---.__________)
        """)

def scissors():
    print("""
            _______
        ---'   ____)____
                  ______)
                __________)
                (____)
        ---.__(___)
        """)

rps()