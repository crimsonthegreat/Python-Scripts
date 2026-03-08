# 8.9
def show_messages(messages):
    """Dispaly list messages"""
    for message in messages:
        print(message)

messages = [
    'I love Python!',
    'Python is the best!',
    'What would you do without Python?'
    ]
show_messages(messages)

# 8.10
def show_messages(messages, sent_messages):
    """Dispaly list messages"""
    while messages:
        current_message = messages.pop()
        print(current_message)
        sent_messages.append(current_message)

def send_messages(sent_messages):
    """Moves messages from messages list to sent messages"""
    print("\nThe following messages have been sent:")
    for sent_message in sent_messages:
        print(sent_message)

messages = [
        'I love Python!',
        'Python is the best!',
        'What would you do without Python?'
        ]
sent_messages = []

print(messages)
print(sent_messages)

show_messages(messages, sent_messages)
send_messages(sent_messages)

print(messages)
print(sent_messages)

# 8.11
messages = [
        'I love Python!',
        'Python is the best!',
        'What would you do without Python?'
        ]
sent_messages = []

show_messages(messages[:], sent_messages)
send_messages(sent_messages)

print(messages)
print(sent_messages)