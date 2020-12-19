import json

with open("D:/folder/тг/result.json", "r", encoding='utf-8') as read_file:
    data = json.load(read_file)

f = open('../files/msg.txt', 'a', encoding='utf-8')
messages = data['messages']

for i in range(0, len(messages)):
    message = messages[i]
    try:
        if str(message['text']).find('type') == -1:
            f.write(str(message['text']) + '\n')
    except KeyError:
        pass
f.close()
