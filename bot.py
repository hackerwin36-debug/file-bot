import telebot
import threading
import time
import os
import json

TOKEN = os.environ['TOKEN']
MASTER = int(os.environ['OWNER'])
bot = telebot.TeleBot(TOKEN)

SECRET = 'give_my_file'
FILE_DATA = 'file.json'
OWNER_DATA = 'owners.json'

def load_owners():
    try:
        with open(OWNER_DATA, 'r') as f:
            return json.load(f).get('owners', [MASTER])
    except:
        return [MASTER]

def save_owners(owners):
    with open(OWNER_DATA, 'w') as f:
        json.dump({'owners': owners}, f)

def load_file():
    try:
        with open(FILE_DATA, 'r') as f:
            return json.load(f).get('file_id')
    except:
        return None

def save_file(fid):
    with open(FILE_DATA, 'w') as f:
        json.dump({'file_id': fid}, f)

OWNERS = load_owners()
FILE_ID = load_file()

def is_owner(uid):
    return uid in OWNERS

def delete_later(cid, mid, sec):
    time.sleep(sec)
    try:
        bot.delete_message(cid, mid)
    except:
        pass

@bot.message_handler(commands=['myid'])
def myid(m):
    bot.reply_to(m, f'Your ID: {m.from_user.id}')

@bot.message_handler(commands=['addowner'])
def addowner(m):
    if m.from_user.id != MASTER:
        bot.reply_to(m, 'Only master can add owners')
        return
    try:
        parts = m.text.split()
        if len(parts) < 2:
            bot.reply_to(m, 'Usage: /addowner ID')
            return
        new = int(parts[1])
        if new not in OWNERS:
            OWNERS.append(new)
            save_owners(OWNERS)
            bot.reply_to(m, f'Owner {new} added!')
        else:
            bot.reply_to(m, 'Already owner')
    except:
        bot.reply_to(m, 'Invalid ID')

@bot.message_handler(commands=['removeowner'])
def removeowner(m):
    if m.from_user.id != MASTER:
        bot.reply_to(m, 'Only master can remove owners')
        return
    try:
        parts = m.text.split()
        if len(parts) < 2:
            bot.reply_to(m, 'Usage: /removeowner ID')
            return
        rem = int(parts[1])
        if rem == MASTER:
            bot.reply_to(m, 'Cannot remove master')
        elif rem in OWNERS:
            OWNERS.remove(rem)
            save_owners(OWNERS)
            bot.reply_to(m, f'Owner {rem} removed!')
        else:
            bot.reply_to(m, 'Not an owner')
    except:
        bot.reply_to(m, 'Invalid ID')

@bot.message_handler(commands=['owners'])
def listowners(m):
    if not is_owner(m.from_user.id):
        bot.reply_to(m, 'Only owners can view')
        return
    txt = 'OWNERS:\n'
    for o in OWNERS:
        if o == MASTER:
            txt += f'- {o} (MASTER)\n'
        else:
            txt += f'- {o}\n'
    bot.reply_to(m, txt)

@bot.message_handler(commands=['upload'])
def upload(m):
    if not is_owner(m.from_user.id):
        bot.reply_to(m, 'Only owners can upload')
        return
    bot.reply_to(m, 'Send me the file')

@bot.message_handler(content_types=['document'])
def handle_doc(m):
    if not is_owner(m.from_user.id):
        bot.reply_to(m, 'Only owners can upload')
        return
    global FILE_ID
    FILE_ID = m.document.file_id
    save_file(FILE_ID)
    botname = bot.get_me().username
    bot.reply_to(m, f'FILE SET!\nFile: {m.document.file_name}\nLink: https://t.me/{botname}?start={SECRET}')

@bot.message_handler(commands=['showfile'])
def showfile(m):
    if not is_owner(m.from_user.id):
        return
    if FILE_ID:
        bot.send_document(m.chat.id, FILE_ID)
    else:
        bot.reply_to(m, 'No file')

@bot.message_handler(commands=['removefile'])
def removefile(m):
    if not is_owner(m.from_user.id):
        return
    global FILE_ID
    FILE_ID = None
    save_file(None)
    bot.reply_to(m, 'File removed')

@bot.message_handler(commands=['status'])
def status(m):
    if not is_owner(m.from_user.id):
        return
    status_text = 'YES' if FILE_ID else 'NO'
    bot.reply_to(m, f'File: {status_text}\nOwners: {len(OWNERS)}')

@bot.message_handler(commands=['start'])
def start(m):
    if not FILE_ID:
        bot.reply_to(m, 'No file available')
        return
    parts = m.text.split()
    if len(parts) > 1 and parts[1] == SECRET:
        bot.send_message(m.chat.id, 'WARNING! File will be deleted in 1 hour! Download now.')
        f = bot.send_document(m.chat.id, FILE_ID)
        threading.Thread(target=delete_later, args=(m.chat.id, f.message_id, 3600)).start()
    elif len(parts) > 1:
        bot.reply_to(m, 'Wrong secret')
    else:
        bot.reply_to(m, 'Use channel link to get file')

@bot.message_handler(commands=['ping'])
def ping(m):
    bot.reply_to(m, 'Pong!')

print('Bot Started!')
print(f'Master Owner: {MASTER}')
print(f'Total Owners: {len(OWNERS)}')
print(f'File Set: {FILE_ID is not None}')
bot.infinity_polling()
