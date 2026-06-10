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

# ========== EMOJI COMMANDS ==========

@bot.message_handler(commands=['myid'])
def myid(m):
    bot.reply_to(m, f'🆔 **Your ID:** `{m.from_user.id}`\n\n👑 Share this with master owner to become owner!', parse_mode='Markdown')

@bot.message_handler(commands=['addowner'])
def addowner(m):
    if m.from_user.id != MASTER:
        bot.reply_to(m, '❌ Only master owner can add owners!', parse_mode='Markdown')
        return
    try:
        parts = m.text.split()
        if len(parts) < 2:
            bot.reply_to(m, '📝 **Usage:** `/addowner ID`\n\nExample: `/addowner 123456789`', parse_mode='Markdown')
            return
        new = int(parts[1])
        if new not in OWNERS:
            OWNERS.append(new)
            save_owners(OWNERS)
            bot.reply_to(m, f'✅ **Owner Added!**\n\n👑 New Owner: `{new}`\n📋 Total Owners: `{len(OWNERS)}`', parse_mode='Markdown')
        else:
            bot.reply_to(m, f'⚠️ `{new}` is already an owner!', parse_mode='Markdown')
    except:
        bot.reply_to(m, '❌ Invalid ID! Use numbers only.', parse_mode='Markdown')

@bot.message_handler(commands=['removeowner'])
def removeowner(m):
    if m.from_user.id != MASTER:
        bot.reply_to(m, '❌ Only master owner can remove owners!', parse_mode='Markdown')
        return
    try:
        parts = m.text.split()
        if len(parts) < 2:
            bot.reply_to(m, '📝 **Usage:** `/removeowner ID`\n\nExample: `/removeowner 123456789`', parse_mode='Markdown')
            return
        rem = int(parts[1])
        if rem == MASTER:
            bot.reply_to(m, '🔥 Cannot remove MASTER owner!', parse_mode='Markdown')
        elif rem in OWNERS:
            OWNERS.remove(rem)
            save_owners(OWNERS)
            bot.reply_to(m, f'🗑️ **Owner Removed!**\n\n👑 Removed: `{rem}`\n📋 Total Owners: `{len(OWNERS)}`', parse_mode='Markdown')
        else:
            bot.reply_to(m, f'⚠️ `{rem}` is not an owner!', parse_mode='Markdown')
    except:
        bot.reply_to(m, '❌ Invalid ID! Use numbers only.', parse_mode='Markdown')

@bot.message_handler(commands=['owners'])
def listowners(m):
    if not is_owner(m.from_user.id):
        bot.reply_to(m, '🔒 Only owners can view this!', parse_mode='Markdown')
        return
    txt = '👑 **OWNERS LIST** 👑\n\n'
    for o in OWNERS:
        if o == MASTER:
            txt += f'⭐ `{o}` (MASTER)\n'
        else:
            txt += f'✅ `{o}`\n'
    txt += f'\n📋 **Total:** `{len(OWNERS)}`'
    bot.reply_to(m, txt, parse_mode='Markdown')

@bot.message_handler(commands=['upload'])
def upload(m):
    if not is_owner(m.from_user.id):
        bot.reply_to(m, '🔒 Only owners can upload files!', parse_mode='Markdown')
        return
    bot.reply_to(m, '📤 **Send me the file**\n\nSupported: Document, Photo, Video, Audio\n\n⏰ File will auto-delete in 1 hour for users!', parse_mode='Markdown')

@bot.message_handler(content_types=['document', 'photo', 'video', 'audio'])
def handle_file(m):
    if not is_owner(m.from_user.id):
        bot.reply_to(m, '🔒 Only owners can upload files!', parse_mode='Markdown')
        return
    
    global FILE_ID
    file_name = "Unknown"
    file_type = "File"
    
    if m.document:
        FILE_ID = m.document.file_id
        file_name = m.document.file_name
        file_type = "📄 Document"
    elif m.photo:
        FILE_ID = m.photo[-1].file_id
        file_name = "Photo.jpg"
        file_type = "🖼️ Photo"
    elif m.video:
        FILE_ID = m.video.file_id
        file_name = m.video.file_name or "Video.mp4"
        file_type = "🎬 Video"
    elif m.audio:
        FILE_ID = m.audio.file_id
        file_name = m.audio.file_name or "Audio.mp3"
        file_type = "🎵 Audio"
    
    save_file(FILE_ID)
    botname = bot.get_me().username
    
    bot.reply_to(
        m,
        f'✅ **FILE SET!**\n\n'
        f'{file_type} `{file_name}`\n'
        f'🆔 ID: `{FILE_ID[:20]}...`\n\n'
        f'🔗 **Channel Link:**\n'
        f`https://t.me/{botname}?start={SECRET}\n\n`
        f'⏰ Users will get file with **1 hour auto-delete**!\n'
        f'👑 You can change file anytime with `/upload`',
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['showfile'])
def showfile(m):
    if not is_owner(m.from_user.id):
        return
    if FILE_ID:
        bot.send_document(m.chat.id, FILE_ID, caption='📁 **Current File in Bot**\n\n✅ This is what users will get!', parse_mode='Markdown')
        bot.reply_to(m, f'✅ File ID: `{FILE_ID[:30]}...`', parse_mode='Markdown')
    else:
        bot.reply_to(m, '❌ **No file set!**\n\nUse `/upload` to set a file.', parse_mode='Markdown')

@bot.message_handler(commands=['removefile'])
def removefile(m):
    if not is_owner(m.from_user.id):
        return
    global FILE_ID
    FILE_ID = None
    save_file(None)
    bot.reply_to(m, '🗑️ **File Removed!**\n\nUsers will now see "No file available" message.', parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status(m):
    if not is_owner(m.from_user.id):
        return
    status_text = '✅ SET' if FILE_ID else '❌ NOT SET'
    emoji = '🟢' if FILE_ID else '🔴'
    bot.reply_to(
        m,
        f'{emoji} **BOT STATUS** {emoji}\n\n'
        f'📁 File: `{status_text}`\n'
        f'👑 Owners: `{len(OWNERS)}`\n'
        f'⭐ Master: `{MASTER}`\n'
        f'⏰ Auto-delete: `1 Hour`\n'
        f'🔄 24/7: `Active`\n'
        f'🎯 Mode: `User gets file via link only`',
        parse_mode='Markdown'
    )

# ========== USER COMMANDS ==========

@bot.message_handler(commands=['start'])
def start(m):
    if not FILE_ID:
        bot.reply_to(
            m,
            '❌ **No File Available!**\n\n'
            '📢 Bot is being setup. Contact owner for more info.\n'
            '👑 Owner will upload file soon.',
            parse_mode='Markdown'
        )
        return
    
    parts = m.text.split()
    if len(parts) > 1 and parts[1] == SECRET:
        # Send warning with emojis
        bot.send_message(
            m.chat.id,
            '⚠️ **⚠️ WARNING! ⚠️** ⚠️\n\n'
            '📁 Ye file **1 GHANTA** baad **AUTO-DELETE** ho jayegi!\n\n'
            '💾 **Abhi download kar lo!**\n'
            '📥 Save karke rakh le, warna baad me nahi milegi!\n\n'
            '⏰ Time remaining: `60 minutes`\n'
            '🔥 OGGY BHAI - CHUMT KA DARINDA',
            parse_mode='Markdown'
        )
        
        # Send file
        f = bot.send_document(
            m.chat.id,
            FILE_ID,
            caption='🔓 **Ye le teri file!**\n\n'
            '⏰ **1 ghanta** hai tere paas!\n'
            '💀 Delete hone se pehle download kar le!\n\n'
            '😈 **OGGY BHAI** - CHUMT KA DARINDA',
            parse_mode='Markdown'
        )
        
        # Start deletion timer
        threading.Thread(target=delete_later, args=(m.chat.id, f.message_id, 3600)).start()
        
    elif len(parts) > 1:
        bot.reply_to(
            m,
            '❌ **GALAT LINK!** ❌\n\n'
            '🔗 Channel se **sahi link** click kar.\n'
            '📢 Direct /start se file nahi milegi!\n\n'
            '👑 Owner se contact karo agar problem hai.',
            parse_mode='Markdown'
        )
    else:
        bot.reply_to(
            m,
            '🤡 **CHUTIYA BANA RHA HAI KYA?** 🤡\n\n'
            '🔗 **Channel me diye LINK** pe CLICK kar, warna file nahi milegi!\n\n'
            '❌ `/start` type karne se kuch nahi hoga.\n'
            '✅ Sirf channel link se file milegi!\n\n'
            '🔥 **OGGY BHAI** - CHUMT KA DARINDA 😈',
            parse_mode='Markdown'
        )

@bot.message_handler(commands=['ping'])
def ping(m):
    bot.reply_to(
        m,
        '🏓 **PONG!** 🏓\n\n'
        '✅ Bot is **ALIVE** and **RUNNING**!\n'
        '🔥 OGGY BHAI mode: **ACTIVE**\n'
        '⏰ 24/7: **ON**\n'
        '📁 File status: `{}`\n\n'
        '😈 CHUMT KA DARINDA is here!'.format('✅ SET' if FILE_ID else '❌ NOT SET'),
        parse_mode='Markdown'
    )

print('='*50)
print('🔥 OGGY BOT ACTIVATED! (EMOJI VERSION)')
print(f'👑 Master Owner: {MASTER}')
print(f'📋 Total Owners: {len(OWNERS)}')
print(f'📁 File Status: {"SET" if FILE_ID else "NOT SET"}')
print('='*50)
bot.infinity_polling()
