import random

import numpy as np


# Обработка исключения для метода getNeuroText()
def try_repeat(func):
    def wrapper(*args, **kwargs):
        count = 10

        while count:
            try:
                return func(*args, **kwargs)
            except UnboundLocalError as e:
                # print('Error:', e)
                count -= 1
    return wrapper


# Вспомогательный метод для следующего
def make_pairs(_ind_words):
    for k in range(len(_ind_words) - 1):
        yield _ind_words[k], _ind_words[k + 1]


# Генератор случайного текста (не ИИ)
def rand_text(amount, words):
    line_array = words

    res_len = amount + 1
    res = ''
    for i in range(0, res_len):
        rand = int(random.random() * len(line_array))
        res = res + line_array[rand] + ' '

    arr_replace = ['.', ',', '\'', '\"', ':', '_', '@', ';']
    for i in range(0, len(arr_replace)):
        res = res.replace(str(arr_replace[i]), '')
    return res.replace('  ', ' ').lower()


# Генерация текста с помощью цепей Маркова
@try_repeat
def get_neuro_text(chatid, amount):
    chatid = str(chatid)
    data = open('./messages/messages' + chatid + '.txt', encoding='utf-8').read()
    ind_words = data.split()

    if len(ind_words) < 50:
        return rand_text(amount, ind_words)
    else:
        pair = make_pairs(ind_words)

        word_dict = {}
        for word_1, word_2 in pair:
            if word_1 in word_dict.keys():
                word_dict[word_1].append(word_2)
            else:
                word_dict[word_1] = [word_2]

        first_word = np.random.choice(ind_words)

        while first_word.islower():
            chain = [first_word]
            n_words = amount
            first_word = np.random.choice(ind_words)

            for i in range(n_words):
                try:
                    chain.append(np.random.choice(word_dict[chain[-1]]))
                except KeyError as e:
                    print(e)
                    pass

        res = ' '.join(chain)

        arr_replace = ['.', ',', '\'', '\"', ':', '_', '@', ';']
        for i in range(0, len(arr_replace)):
            res = res.replace(str(arr_replace[i]), '')
        return res.replace('  ', ' ').lower()
