import telebot
import PySimpleGUI as sg

bot = telebot.TeleBot(open('../files/api.txt', encoding='utf-8').read())

f = open('../files/chats.txt', 'r', encoding='utf-8')
text = f.read()
arr = text.split('\n')
arr = arr[:len(arr) - 1]

choices1 = []
choices2 = []
k = 0
for _ in arr:
    choices1.append(arr[k].rpartition(' - ')[0])
    choices2.append(arr[k].rpartition(' - ')[2])
    k += 1


def single(my_message, chat_id):
    try:
        bot.send_message(chat_id=chat_id, text=my_message)
    except telebot.apihelper.ApiTelegramException:
        print('Bot is banned :(')


def sticker(my_message, chat_id):
    try:
        bot.send_sticker(chat_id, my_message)
    except telebot.apihelper.ApiTelegramException:
        print('Bot is banned :(')


def all_chats(my_message):
    try:
        j = 0
        for _ in arr:
            arr[j] = arr[j].rpartition(' - ')[0]
            bot.send_message(chat_id=arr[j], text=my_message)
            j += 1
    except telebot.apihelper.ApiTelegramException:
        print('Bot is banned :(')


layout = [
    [sg.Text('Input message'), sg.InputText()
     ],
    [sg.Text('Select a chat'), sg.Combo(choices2),
     sg.Checkbox('Select all'), sg.Checkbox('Sticker')
     ],
    [sg.Output(size=(88, 20))],
    [sg.Button('Send'), sg.Button('Exit')]
]
window = sg.Window('Send message', layout)

while True:
    event, values = window.read()
    # print(values)
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Send':
        if values[0]:
            message = values[0]
            if values[2]:
                all_chats(message)
                print('Message is sent to all chats')
            elif values[1]:
                chatname = values[1]
                i = 0
                for _ in choices2:
                    if chatname == choices2[i]:
                        break
                    else:
                        i += 1
                if values[3]:
                    sticker(message, choices1[i])
                else:
                    single(message, choices1[i])
                print('Message is sent to ' + chatname)
            else:
                print('Select a chat!')
        elif event == 'Exit':
            break
        else:
            print('Please input a message')
