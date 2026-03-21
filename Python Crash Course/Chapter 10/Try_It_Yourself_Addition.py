from pathlib import Path

# 10.6/ 10.7 create a while loop with a try/except to handle 
# if users puts in letters or characters instead of numbers
# use q to quit the loop
print("Please enter two numbers and I will add them.")
print("Enter 'q' to quit")
while True:
    first_num = input("\nPlease enter your first number: ")
    if first_num == 'q':
        break
    second_num = input("Please enter your second number: ")
    if second_num == 'q':
        break

    try:
        addition = int(first_num) + int(second_num)
    except ValueError:
        print("Please enter numbers, letters and characters will not work")
    else:
        print(addition)

# 10.8 read the files cats and dogs and output the contents
# add a try/except block to handle a missing file
filenames = ['cats.txt', 'dogs.txt']
for filename in filenames:
    path = Path(filename)
    
    try:
        contents = path.read_text()
    except FileNotFoundError:
        print(f"The file {path} was no found.")
    else:
        print(f"\nThe {filename.strip('.txt')} names are:")
        print(contents.title())

# 10.9 silent exception for file no found
print("\nTesting a silent exception.")
filenames = ['cats.txt', 'dogs.txt']
for filename in filenames:
    path = Path(filename)
    
    try:
        contents = path.read_text()
    except FileNotFoundError:
        pass
    else:
        print(f"\nThe {filename.strip('.txt')} names are:")
        print(contents.title())

# 10.10 find common words in a given text
filenames = ['alice.txt', 'moby_dick.txt', 'little_women.txt']
for filename in filenames:
    path = Path(filename)

    try:
        contents = path.read_text(encoding='utf-8')
    except:
        print(f"The file {path} was not found.")
    else:
        print(f"\nThe count of any word with the in it from file {path}:")
        count_the = contents.lower().count('the')
        print(count_the)
        print(f"The count of only the word the in file {path}")
        count_the = contents.lower().count('the ')
        print(count_the)