from pathlib import Path

# 10.4 prompt for guest's name and add it to guest.txt
path = Path('guests.txt')
guest = input("Please enter your name so it can be added to the guest book: ")
path.write_text(guest)

# 10.5 prompt for multiple guests and add to guest_book.txt
path = Path('guest_book.txt')
guest_book = ""
guest_count = 0
while guest_count < 5:
    guest = input("Please enter your name so it "
                  "can be added to the guest book: ")
    guest_book += f"{guest}\n"
    guest_count += 1

path.write_text(guest_book)
book = path.read_text()
print(book)