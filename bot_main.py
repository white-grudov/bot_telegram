import os
import telebot
import random
from functions import stuff, text_gen, image_gen

bot = telebot.TeleBot(open('./files/api.txt', encoding='utf-8').read())


# Команда /help
@bot.message_handler(commands=['help'])
def send_image(message):
    bot.send_message(message.chat.id,
                     open('./files/help.txt', encoding='utf-8').read(), parse_mode='HTML')


# Личные сообщения
@bot.message_handler(content_types=['text'])
def private_messages(message):
    reply = 'Я предназначен для использования только в групповых чатах! ' \
            'Если хочешь узнать, что я делаю, напиши /help.'
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, reply)
    else:
        skobka(message)


# Скобка 1
@bot.message_handler(content_types=['text'])
def skobka(message):
    if message.text.startswith(')'):
        bot.send_message(message.chat.id, message.text, reply_to_message_id=message.id)
    else:
        skobka_sad(message)


# Скобка 2
@bot.message_handler(content_types=['text'])
def skobka_sad(message):
    if message.text.startswith('('):
        bot.send_message(message.chat.id, 'не грусти', reply_to_message_id=message.id)
    else:
        just_pin(message)


# Просто пин бота
@bot.message_handler(content_types=['text'])
def just_pin(message):
    if message.text == '@danekbel_chatbot':
        try:
            # Ответ на текст
            if message.reply_to_message.content_type == 'text':
                image_gen.image(message.chat.title,
                                message.chat.id,
                                message.from_user.username,
                                message.from_user.id,
                                message.reply_to_message.text, 2)
                bot.send_photo(message.chat.id, open('./images/result.png', 'rb'))

            # Ответ на картинку
            elif message.reply_to_message.content_type == 'photo':
                file_info = \
                    bot.get_file(message.reply_to_message.photo[len(message.reply_to_message.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                with open('./images/reply.png', 'wb') as new_file:
                    new_file.write(downloaded_file)

                image_gen.image(message.chat.title,
                                message.chat.id,
                                message.from_user.username,
                                message.from_user.id, '', 3)
                bot.send_photo(message.chat.id, open('./images/result.png', 'rb'))

            # Ответ на стикер
            elif message.reply_to_message.content_type == 'sticker':
                file_info = bot.get_file(message.reply_to_message.sticker.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                with open('./images/reply.png', 'wb') as new_file:
                    new_file.write(downloaded_file)

                image_gen.image(message.chat.title,
                                message.chat.id,
                                message.from_user.username,
                                message.from_user.id, '', 3)
                bot.send_photo(message.chat.id, open('./images/result.png', 'rb'))

        # Исключение
        except AttributeError:
            bot.send_message(message.chat.id, 'Ой-ой! Ты сделал что-то не то...')
        except telebot.apihelper.ApiTelegramException:
            print('Bot is banned :(')
        except Exception as e:
            print(e)
    else:
        pin_with_text(message)


# Пин с текстом
@bot.message_handler(content_types=['text'])
def pin_with_text(message):
    if message.text.startswith('@danekbel_chatbot'):
        try:
            # Ответ на текст
            if message.reply_to_message.content_type == 'text':
                bot.send_message(message.chat.id, 'Ответь на картинку!', reply_to_message_id=message.id)

            # Ответ на картинку
            elif message.reply_to_message.content_type == 'photo':
                file_info = \
                    bot.get_file(message.reply_to_message.photo[len(message.reply_to_message.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                with open('./images/reply.png', 'wb') as new_file:
                    new_file.write(downloaded_file)

                text = message.text.replace('@danekbel_chatbot', '', 1)
                image_gen.image(message.chat.title,
                                message.chat.id,
                                message.from_user.username,
                                message.from_user.id, text, 4)
                bot.send_photo(message.chat.id, open('./images/result.png', 'rb'))

            # Ответ на стикер
            elif message.reply_to_message.content_type == 'sticker':
                file_info = bot.get_file(message.reply_to_message.sticker.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                with open('./images/reply.png', 'wb') as new_file:
                    new_file.write(downloaded_file)

                text = message.text.replace('@danekbel_chatbot', '', 1)
                image_gen.image(message.chat.title,
                                message.chat.id,
                                message.from_user.username,
                                message.from_user.id, text, 4)
                bot.send_photo(message.chat.id, open('./images/result.png', 'rb'))

        # Исключение
        except AttributeError:
            bot.send_message(message.chat.id, 'Ой-ой! Ты сделал что-то не то...')
        except telebot.apihelper.ApiTelegramException:
            print('Bot is banned :(')
        except Exception as e:
            print(e)
    else:
        manual_gen(message)


# Команды
@bot.message_handler(content_types=['text'])
def manual_gen(message):
    #  Генерация картинки
    try:
        if message.text == 'D i':
            image_gen.image(message.chat.title,
                            message.chat.id,
                            message.from_user.username,
                            message.from_user.id, '', 1)
            bot.send_photo(message.chat.id, open('./images/result.png', 'rb'))

        #  Генерация текста
        elif message.text == 'D t':
            bot.send_message(message.chat.id,
                             text_gen.get_neuro_text(message.chat.id, random.randint(0, 5) + 7))
            stuff.write_to_log('gen_text  ',
                               message.chat.title,
                               message.chat.id,
                               message.from_user.username,
                               message.from_user.id)
        elif message.text == 'D p':
            prediction = 'Ваше предсказание✨:\n<i>' + \
                         text_gen.get_neuro_text(-1488, random.randint(0, 3) + 11) + '</i>'
            bot.send_message(message.chat.id, prediction, parse_mode='HTML')
            stuff.write_to_log('predict  ',
                               message.chat.title,
                               message.chat.id,
                               message.from_user.username,
                               message.from_user.id)
        else:
            save_and_gen(message)
    except telebot.apihelper.ApiTelegramException:
        print('Bot is banned :(')


# Сохранение текста и генерация
@bot.message_handler(content_types=['text'])
def save_and_gen(message):
    stuff.write_to_file(message.text,
                        message.chat.title,
                        message.chat.id,
                        message.from_user.username,
                        message.from_user.id)
    rand = random.randint(1, 100)
    print(rand)
    try:
        if rand == 1:
            image_gen.image(message.chat.title,
                            message.chat.id,
                            message.from_user.username,
                            message.from_user.id, '', 1)
            bot.send_photo(message.chat.id, open('./images/result.png', 'rb'))
        if rand == 2:
            bot.send_message(message.chat.id,
                             text_gen.get_neuro_text(message.chat.id, random.randint(0, 5) + 7))
            stuff.write_to_log('gen_text ',
                               message.chat.title,
                               message.chat.id,
                               message.from_user.username,
                               message.from_user.id)
        if message.from_user.id == 347398049:
            if rand == 3:
                bot.send_message(message.chat.id, 'привет дима', reply_to_message_id=message.id)
    except telebot.apihelper.ApiTelegramException:
        print('Bot is banned :(')


# Фото с текстом
@bot.message_handler(content_types=['photo'])
def image_with_pin(message):
    print('test')
    try:
        if message.caption == '@danekbel_chatbot':
            file_info = \
                bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('./images/reply.png', 'wb') as new_file:
                new_file.write(downloaded_file)

            image_gen.image(message.chat.title,
                            message.chat.id,
                            message.from_user.username,
                            message.from_user.id, '', 3)
            bot.send_photo(message.chat.id, open('./images/result.png', 'rb'))
        elif message.caption.startswith('@danekbel_chatbot'):
            file_info = \
                bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('./images/reply.png', 'wb') as new_file:
                new_file.write(downloaded_file)

            text = message.caption.replace('@danekbel_chatbot', '', 1)
            image_gen.image(message.chat.title,
                            message.chat.id,
                            message.from_user.username,
                            message.from_user.id, text, 4)
            bot.send_photo(message.chat.id, open('./images/result.png', 'rb'))
        else:
            handle_docs_photo(message)
    except Exception as e:
        print(e)
        handle_docs_photo(message)


# Сохранение фото
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    stuff.write_to_log('photo   ',
                       message.chat.title,
                       message.chat.id,
                       message.from_user.username,
                       message.from_user.id)
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        path_arr = file_info.file_path.split('/')
        path = path_arr[0] + '/' + str(message.chat.id) + '/' + path_arr[1]

        src = './' + path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

    except Exception as e:
        print(e)


# Сохранение стикеров
@bot.message_handler(content_types=['sticker'])
def handle_docs_sticker(message):
    #  Исключение для Чата ФИ
    if message.from_user.id == 419467462:
        bot.send_message(message.chat.id, '<i>Beware of that curious performance!</i>', parse_mode='HTML')
    else:
        try:
            stuff.write_to_log('sticker   ',
                               message.chat.title,
                               message.chat.id,
                               message.from_user.username,
                               message.from_user.id)

            file_info = bot.get_file(message.sticker.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            path_arr = file_info.file_path.split('/')
            path = './photos/' + str(message.chat.id) + '/' + path_arr[1]

            src = './' + path
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            length = len(src)
            os.rename(src, src[:length - 4] + 'png')
        except Exception as e:
            print(e)


bot.polling()
