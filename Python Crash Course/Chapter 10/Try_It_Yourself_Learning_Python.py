from pathlib import Path

# 10.1 reading from files
path = Path('learning_python.txt')
contents = path.read_text().rstrip()
print(f"{contents}\n")

lines = contents.splitlines()
for line in lines:
    print(line)

# 10.2 using the replace method
lines = contents.splitlines()
for line in lines:
    message = line.replace('python', 'c')
    print(message)

# 10.3 simplify the code
for line in contents.splitlines():
    print(line)