import telebot

def admin_creator(message):
    administrator = Admin(message)
    return administrator

class Admin:

    def __init__(self, message):
        self.id = message.chat_id
        self.name = message.chat_id.username


def admin_list(id):
    adm = []
    with open('adminlist', 'r') as adminlist:
        for admin in adminlist:
            adm.append(int(admin))

    if id in adm:
        return True


def add_admin(id):
    with open('adminlist', 'a') as adminlist:
        adminlist.write(id + '\n')

