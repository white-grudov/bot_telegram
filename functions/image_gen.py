import os
import random
import PIL

from PIL import ImageDraw, ImageFont, Image
from functions import stuff, text_gen


# Центрирует текст в изображении
def text_centered(img, text, width, size, pos):
    ImageDraw.Draw(img)
    font = ImageFont.truetype("./images/font.ttf", size)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(text, font)
    draw.text(((width - w) / 2, pos), text, fill='white', font=font)
    return w


# mode = 1 - случайный текст, случайная картинка
# mode = 2 - свой текст, случайная картинка
# mode = 3 - случайный текст, своя картинка
# mode = 4 - свой текст, своя картинка
def image(chatname, chatid, username, userid, text, mode):
    try:
        if mode != 2 and mode != 4:
            phrase_1 = text_gen.get_neuro_text(chatid, random.randint(0, 3))
            phrase_2 = text_gen.get_neuro_text(chatid, random.randint(0, 6))
        else:
            phrase_1 = text
            phrase_2 = ''

        W = 1280
        H = 230
        text_image = Image.new('RGB', (W, H), color='#000000')

        if mode != 2 and mode != 4:
            val1 = text_centered(text_image, phrase_1, W, 100, 0)
            val2 = text_centered(text_image, phrase_2, W, 40, 120)
        else:
            val1 = text_centered(text_image, phrase_1, W, 100, 50)
            val2 = 0

        main = Image.open('./images/source.png')

        if val1 > 1200 or val2 > 1200:
            if val1 > val2:
                new_w = val1
            else:
                new_w = val2
            big_text = Image.new('RGB', (new_w, H), color='#000000')

            if mode != 2 and mode != 4:
                text_centered(big_text, phrase_1, new_w, 100, 0)
                text_centered(big_text, phrase_2, new_w, 40, 120)
            else:
                text_centered(big_text, phrase_1, new_w, 100, 50)

            big_text.save('./images/help.png')
            im_test = Image.open('./images/help.png')
            im_test = im_test.resize((W - 10, H))

            main.paste(im_test, (10, 800))
        else:
            main.paste(text_image, (0, 800))

        if mode == 3 or mode == 4:
            im1 = Image.open('./images/reply.png')
        else:
            im1 = Image.open('./photos/' + str(chatid) + '/' + random.choice(os.listdir('./photos/' + str(chatid))))
        new_size = (1025, 683)
        im1 = im1.resize(new_size)
        main.paste(im1, (127, 85))

        stuff.write_to_log('gen_image', chatname, chatid, username, userid)

        text_image.save('./images/text.png')
        main.save('./images/result.png')
    except FileNotFoundError:
        pass
    except PIL.UnidentifiedImageError:
        bonus = Image.open('./images/bonus.jpg')
        bonus.save('./images/result.png')
    except TypeError:
        pass
