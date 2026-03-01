#Name and Personal Message
First_name = 'Crimson'
Last_name = 'TheGreat'
full_name = f'{First_name}{Last_name}'
print(full_name.title())
personal_message = f"Hello, {full_name.title()}! \nWould you like to learn some Python today?"
print(personal_message)

#Famous Quote
quote = f'Thomas Edison once said, "Our greatest weakness lies in giving up. The most certain way to succeed is always to try just one more time."'
print(quote)
famous_person = 'Thomas Edison'
message = f'{famous_person} once said, "Our greatest weakness lies in giving up. The most certain way to succeed is always to try just one more time."'
print(message)

#Strip Actions
First_name = '   Crimson   '
print(First_name.rstrip())
print(First_name.lstrip())
print(First_name.strip())

#Remove Prefixes
url = 'https://www.python.org'
print(url.removeprefix('https://'))

#Remove Suffixes
filename = 'python.exe'
print(filename.removesuffix('.exe'))
