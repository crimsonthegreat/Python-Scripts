favorite_language = {
    'jen' : 'python',
    'sarah' : 'c',
    'edward' : 'rust',
    'phil' : 'python',
    }

language = favorite_language['sarah'].title()
print(f"Sarah's favorite language is {language}")

favorite_language = {
    'jen' : 'python',
    'sarah' : 'c',
    'edward' : 'rust',
    'phil' : 'python',
    }

for name, language in favorite_language.items():
    print(f"{name.title()}'s favorite language is {language.title()}")

for name in favorite_language.keys():
    print(name.title())

friends = ['phil', 'sarah']
for name in favorite_language.keys():
    print(f'Hi {name.title()}')

    if name in friends:
        language = favorite_language[name].title()
        print(f'\t{name.title()}, I see you love {language}!')
    
    if 'erin' not in favorite_language:
        print('Erin please take our poll!\n')
    
for name in sorted(favorite_language.keys()):
    print(f'{name.title()}, thank you for taking our poll')

print('\nThe following languages have been mentioned:')
for language in favorite_language.values():
    print(language.title())

print('\nThe following languages have been mentioned:')
for language in set(favorite_language.values()):
    print(language.title())

favorite_language = {
    'jen' : ['python', 'rust'],
    'sarah' : ['c'],
    'edward' : ['rust', 'go'],
    'phil' : ['python', 'haskell'],
    }

for name, languages in favorite_language.items():
    print(f"\n{name.title()}'s favorite languages are:")
    for language in languages:
        print(f'\t{language.title()}')