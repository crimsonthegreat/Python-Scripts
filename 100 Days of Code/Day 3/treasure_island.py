print('''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/[TomekK]
*******************************************************************************
''')

def left_right():
    print("You have made it to treasure island and must now find the treasure!")
    print("Upon arrival you find a diveregent path, you must choose" 
        " left or right.")

    while True:
        user_input = input("[left/right]\n")

        if user_input == 'left' or user_input == 'Left':
            print("You walk all day and it begins to get dark.")
            print("You have the option to wait out the night or keep going.")
            user_input = input("[wait/go]\n")
            wait_go_one(user_input)
            break

        elif user_input == 'right' or user_input == 'Right':
            print("You come to a wall with rocks jutting out.")
            print("You can choose to turn back or climb the wall.")
            user_input = input("[climb/leave]")
            climb_leave(user_input)
            break
        else:
            print("Please enter left or right...")

def wait_go_one(user_input):
    while True:
        if user_input == 'wait' or user_input== 'Wait':
            print("It is now day light and you can see again.")
            print("You can choose to continue on the path or wait again.")
            user_input = input("[wait/go]\n")
            wait_go_two(user_input)
            break
        elif user_input == 'go' or user_input == 'Go':
            print("It is to dark to see and you fall into a trap.")
            print("Game over!")
            quit()
        else:
            print("Please enter wait or go...")

def wait_go_two(user_input):
    while True:
        if user_input == 'wait' or user_input== 'Wait':
            print("You end up waiting forever and never leaving.")
            print("Game over!")
            quit()
        elif user_input == 'go' or user_input == 'Go':
            print("You move along the path and find where a trap would have " 
            "gotten you if you had left the night before.")
            print("Going further down the path reveals a cave that shimmers"
            " in the daylight.")
            print("You must chose to enter or stay outside.")
            user_input = input("[stay/enter]")
            stay_enter(user_input)
        else:
            print("Please enter wait or go...")

def stay_enter(user_input):
    while True:
        if user_input == 'stay' or user_input == 'Stay':
            print("A storm rolls in and you are struck by lightning!")
            print("Game over!")
            quit()
        elif user_input == 'enter' or user_input == 'Enter':
            print("Entering the cave reveals a large treasure trove!")
            print("You have found the treasure and have won the game!")
            print("Congratulations!")
            quit()
        else:
            print("Please enter stay or enter...")

def climb_leave(user_input):
    while True:
        if user_input == 'climb' or user_input == 'Climb':
            print("The rocks are slick and you only make it half way up before "
            "slipping and falling to your end.")
            print("Game over!")
            quit()
        elif user_input == 'leave' or user_input == 'Leave':
            print("You go back to the starting area...")
            left_right(user_input)
        else:
            print("Please enter climb or leave...")

left_right()
