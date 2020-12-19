import os
import time


def write_to_file(text, chatname, chatid, username, userid):
    try:
        if username is None:
            username = userid

        chatid, userid = str(chatid), str(userid)

        if text[0] == '/':
            pass
        else:
            f = open('./messages/messages' + chatid + '.txt', 'a', encoding='utf-8')
            try:
                f.write(text + '\n')
            except UnicodeEncodeError:
                error_log('Text is not written', chatname, username, userid)
            f.close()
            write_to_log('new_text ', chatname, chatid, username, userid)
    except TypeError:
        error_log('Text is not written', chatname, username, userid)


def new_dir(chatname, chatid):
    ch = open('./files/chats.txt', 'r', encoding='utf-8')
    ch_text = ch.read()
    ch.close()
    ch = open('./files/chats.txt', 'a', encoding='utf-8')
    ch_add = '\n' + str(chatid) + ' - ' + chatname
    try:
        ch_text.index(chatid)
        arr = ch_text.split('\n')
        if ch_text.find(chatname) == -1:
            for i in range(0, len(arr)):
                if arr[i].find(chatid) != -1:
                    arr[i] = str(chatid) + ' - ' + chatname
            f = open('./files/chats.txt', 'w', encoding='utf-8')
            for k in range(0, len(arr)):
                if k == 0:
                    f.write(arr[k])
                else:
                    f.write('\n' + arr[k])
            f.close()
    except ValueError:
        ch.write(ch_add)
        ch.close()
        os.mkdir('./photos/' + str(chatid))


def write_to_log(text, chatname, chatid, username, userid):
    text, chatname, chatid, username, userid = str(text), str(chatname), str(chatid), str(username), str(userid)

    new_dir(chatname, chatid)

    print(text + ' - ' + chatname + ' - ' + username)
    res = text + ' - ' + chatname + ' - ' + username + ' - ' + userid

    f = open('./files/log.txt', 'a', encoding='utf-8')
    f.write(time.ctime() + ' - ' + res + '\n')
    f.close()


def error_log(text, chatname, username, userid):
    userid = str(userid)
    print(text + ' - ' + chatname + ' - ' + username)
    res = 'Error! ' + text + ' - ' + chatname + ' - ' + username + ' - ' + userid

    f = open('./files/log.txt', 'a', encoding='utf-8')
    f.write(time.ctime() + ' - ' + res + '\n')
    f.close()


def console_log(text):
    f = open('./files/console.txt', 'w')
    f.write(text)
    f.close()
    print(text)
