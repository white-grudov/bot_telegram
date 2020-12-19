import random


# Генератор случайного текста (не ИИ)
def randLine(chat_id, amount1, amount2):
    chat_id = str(chat_id)

    f = open('messages/messages' + chat_id + '.txt', 'r', encoding='utf-8')
    file = f.read()

    line_array = file.split()

    res_len = random.randint(1, amount1) + amount2
    res = ''
    for i in range(0, res_len):
        rand = int(random.random() * len(line_array))
        res = res + line_array[rand] + ' '

    arr_replace = ['.', ',', '\'', '\"', ':', '_', '@', ';']
    for i in range(0, len(arr_replace)):
        res = res.replace(str(arr_replace[i]), '')
    return res.replace('  ', ' ').lower()
