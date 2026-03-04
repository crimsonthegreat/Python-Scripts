users = [ 'admin', 'jsmith', 'jdoe', 'yoda', 'frodo']

for user in users:
    if 'admin' in user:
        print('Hello admin, would you like to see the daily report?')
    else:
        print(f'Hello {user} thank you for logging in')

users = []

if users:
    for user in users:
        if 'admin' in user:
            print('Hello admin, would you like to see the daily report?')
        else:
            print(f'Hello {user} thank you for logging in')
else:
    print('\nWe need to find some users\n')

current_users = [ 'admin', 'JSMITH', 'jdoe', 'yoda', 'frodo']

new_users = ['jsmith', 'JDOE', 'samwise', 'darth vader', 'mando']

if current_users:
    current_user_lower = []
    for current_user in current_users:
        current_user_lower.append(current_user.lower())
    for new_user in new_users:
        if new_user.lower() in current_user_lower:
            print('You will need to create a new username')
        else:
            print(f'{new_user} is available')
else:
    print('\nNo users found!\n')

numbers = list(range(1, 10))

for number in numbers:
    if number == 1:
        print(f'{number}st')
    elif number == 2:
        print(f'{number}nd')
    elif number == 3:
        print(f'{number}rd')
    else:
        print(f'{number}th')
    