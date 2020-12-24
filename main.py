import os
import telebot
import random

from functions import stuff, text_gen, image_gen
from config import TOKEN, HELP, REPLY, START

bot = telebot.TeleBot(TOKEN)


def download(m, mode):
    # Просто фото
    if mode == 1:
        file_info = bot.get_file(m.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        name = file_info.file_path.split('/')[1]
        with open('./photos/' + str(m.chat.id) + '/' + name, 'wb') as new_file:
            new_file.write(downloaded_file)
    # Фото в реплае
    elif mode == 2:
        file_info = bot.get_file(m.reply_to_message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('./images/reply.png', 'wb') as new_file:
            new_file.write(downloaded_file)
    # Просто стикер
    elif mode == 3:
        file_info = bot.get_file(m.sticker.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        name = file_info.file_path.split('/')[1]
        path = './photos/' + str(m.chat.id) + '/' + name
        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
        length = len(path)
        os.rename(path, path[:length - 4] + 'png')
    # Стикер в реплае
    elif mode == 4:
        file_info = bot.get_file(m.reply_to_message.sticker.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('./images/reply.png', 'wb') as new_file:
            new_file.write(downloaded_file)
    # Фото и текст
    elif mode == 5:
        file_info = bot.get_file(m.photo[len(m.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('./images/reply.png', 'wb') as new_file:
            new_file.write(downloaded_file)


# Команда /start
@bot.message_handler(commands=['start'])
def start_command(m):
    bot.send_message(m.chat.id, START, parse_mode='HTML')


# Команда /help
@bot.message_handler(commands=['help'])
def help_command(m):
    bot.send_message(m.chat.id, HELP, parse_mode='HTML')


# Личные сообщения
@bot.message_handler(content_types=['text'])
def private_messages(m):
    if m.chat.type == 'private':
        bot.send_message(m.chat.id, REPLY)
    else:
        skobka(m)


# Скобка 1
@bot.message_handler(content_types=['text'])
def skobka(m):
    if m.text.startswith(')'):
        bot.send_message(m.chat.id, m.text, reply_to_message_id=m.id)
    else:
        skobka_sad(m)


# Скобка 2
@bot.message_handler(content_types=['text'])
def skobka_sad(m):
    if m.text.startswith('(') and not m.text.endswith(')'):
        bot.send_message(m.chat.id, 'не грусти', reply_to_message_id=m.id)
    else:
        just_pin(m)


# Просто пин бота
@bot.message_handler(content_types=['text'])
def just_pin(m):
    if m.text == '@danekbel_chatbot':
        try:
            # Ответ на текст
            if m.reply_to_message.content_type == 'text':
                text = m.reply_to_message.text
                image_gen.image(m.chat.title, m.chat.id, m.from_user.username, m.from_user.id, text, 2)
                bot.send_photo(m.chat.id, open('./images/result.png', 'rb'))
            # Ответ на картинку
            elif m.reply_to_message.content_type == 'photo':
                download(m, 2)
                image_gen.image(m.chat.title, m.chat.id, m.from_user.username, m.from_user.id, '', 3)
                bot.send_photo(m.chat.id, open('./images/result.png', 'rb'))
            # Ответ на стикер
            elif m.reply_to_message.content_type == 'sticker':
                download(m, 4)
                image_gen.image(m.chat.title, m.chat.id, m.from_user.username, m.from_user.id, '', 3)
                bot.send_photo(m.chat.id, open('./images/result.png', 'rb'))
        # Исключение
        except AttributeError:
            bot.send_message(m.chat.id, 'Ой-ой! Ты сделал что-то не то...')
        except telebot.apihelper.ApiTelegramException:
            print('Bot is banned :(')
        except Exception as e:
            print('Просто пин', e)
    else:
        pin_with_text(m)


# Пин с текстом
@bot.message_handler(content_types=['text'])
def pin_with_text(m):
    if m.text.startswith('@danekbel_chatbot'):
        try:
            # Ответ на текст
            if m.reply_to_message.content_type == 'text':
                bot.send_message(m.chat.id, 'Ответь на картинку!', reply_to_message_id=m.id)
            # Ответ на картинку
            elif m.reply_to_message.content_type == 'photo':
                download(m, 2)
                text = m.text.replace('@danekbel_chatbot', '', 1)
                image_gen.image(m.chat.title, m.chat.id, m.from_user.username, m.from_user.id, text, 4)
                bot.send_photo(m.chat.id, open('./images/result.png', 'rb'))
            # Ответ на стикер
            elif m.reply_to_message.content_type == 'sticker':
                download(m, 4)
                text = m.text.replace('@danekbel_chatbot', '', 1)
                image_gen.image(m.chat.title, m.chat.id, m.from_user.username, m.from_user.id, text, 4)
                bot.send_photo(m.chat.id, open('./images/result.png', 'rb'))
        # Исключение
        except AttributeError:
            bot.send_message(m.chat.id, 'Ой-ой! Ты сделал что-то не то...')
        except telebot.apihelper.ApiTelegramException:
            print('Bot is banned :(')
        except Exception as e:
            print('Пин с текстом', e)
    else:
        manual_gen(m)


# Команды
@bot.message_handler(content_types=['text'])
def manual_gen(m):
    try:
        # Генерация картинки
        if m.text == 'D i':
            image_gen.image(m.chat.title, m.chat.id, m.from_user.username, m.from_user.id, '', 1)
            bot.send_photo(m.chat.id, open('./images/result.png', 'rb'))
        # Генерация текста
        elif m.text == 'D t':
            bot.send_message(m.chat.id, text_gen.get_neuro_text(m.chat.id, random.randint(0, 5) + 8))
            stuff.write_to_log('gen_text  ', m.chat.title, m.chat.id, m.from_user.username, m.from_user.id)
        # Генерация предсказания
        elif m.text == 'D p':
            prediction = 'Ваше предсказание✨:\n<i>' + \
                         text_gen.get_neuro_text(-1488, random.randint(0, 3) + 12) + '</i>'
            bot.send_message(m.chat.id, prediction, parse_mode='HTML')
            stuff.write_to_log('predict  ', m.chat.title, m.chat.id, m.from_user.username, m.from_user.id)
        else:
            save_and_gen(m)
    except telebot.apihelper.ApiTelegramException:
        print('Bot is banned :(')
    except Exception as e:
        print('Команды', e)


# Сохранение текста и генерация
@bot.message_handler(content_types=['text'])
def save_and_gen(m):
    stuff.write_to_file(m.text, m.chat.title, m.chat.id, m.from_user.username, m.from_user.id)
    rand = random.randint(1, 100)
    print(rand)
    try:
        if rand == 1:
            image_gen.image(m.chat.title, m.chat.id, m.from_user.username, m.from_user.id, '', 1)
            bot.send_photo(m.chat.id, open('./images/result.png', 'rb'))
        if rand == 2:
            bot.send_message(m.chat.id, text_gen.get_neuro_text(m.chat.id, random.randint(0, 5) + 8))
            stuff.write_to_log('gen_text ', m.chat.title, m.chat.id, m.from_user.username, m.from_user.id)
    except telebot.apihelper.ApiTelegramException:
        print('Bot is banned :(')
    except Exception as e:
        print('Текст и ген', e)


# Фото с текстом
@bot.message_handler(content_types=['photo'])
def image_with_pin(m):
    print('test')
    try:
        if m.caption == '@danekbel_chatbot':
            download(m, 5)
            image_gen.image(m.chat.title, m.chat.id, m.from_user.username, m.from_user.id, '', 3)
            bot.send_photo(m.chat.id, open('./images/result.png', 'rb'))
        elif m.caption.startswith('@danekbel_chatbot'):
            download(m, 5)
            text = m.caption.replace('@danekbel_chatbot', '', 1)
            image_gen.image(m.chat.title, m.chat.id, m.from_user.username, m.from_user.id, text, 4)
            bot.send_photo(m.chat.id, open('./images/result.png', 'rb'))
        else:
            handle_docs_photo(m)
    except Exception as e:
        print(e)
        handle_docs_photo(m)


# Сохранение фото
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(m):
    stuff.write_to_log('photo    ', m.chat.title, m.chat.id, m.from_user.username, m.from_user.id)
    try:
        download(m, 1)
    except Exception as e:
        print(e)


# Сохранение стикеров
@bot.message_handler(content_types=['sticker'])
def handle_docs_sticker(m):
    if m.sticker.is_animated:
        pass
    else:
        try:
            stuff.write_to_log('sticker  ', m.chat.title, m.chat.id, m.from_user.username, m.from_user.id)
            download(m, 3)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    bot.polling()
