import telebot

bot = telebot.TeleBot(open('../files/api.txt', encoding='utf-8').read())


@bot.message_handler(content_types=['photo'])
def test(message):
    print(message)


bot.polling()
