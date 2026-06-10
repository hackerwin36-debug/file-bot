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
            data = json.load(f)
            return data.get('file_id')
    except:
        return None

def save_file(fid):
    with open(FILE_DATA, 'w') as f:
        json.dump({'file_id': fid}, f)

OWNERS = load_owners()
FILE_ID = load_file()

def is_owner(uid):
    return uid in OWNERS

def delete_later(chat_id, message_id, delay):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Delete error: {e}")

# ========== OWNER COMMANDS ==========

@bot.message_handler(commands=['myid'])
def myid(m):
    bot.reply_to(m, f'🆔 **Your ID:** `{m.from_user.id}`', parse_mode='Markdown')

@bot.message_handler(commands=['addowner'])
def addowner(m):
    if m.from_user.id != MASTER:
        bot.reply_to(m, '❌ Only master owner can add owners!', parse_mode='Markdown')
        return
    try:
        parts = m.text.split()
        if len(parts) < 2:
            bot.reply_to(m, '📝 Usage: `/addowner ID`', parse_mode='Markdown')
            return
        new = int(parts[1])
        if new not in OWNERS:
            OWNERS.append(new)
            save_owners(OWNERS)
            bot.reply_to(m, f'✅ Owner `{new}` added! Total: {len(OWNERS)}', parse_mode='Markdown')
        else:
            bot.reply_to(m, f'⚠️ `{new}` is already an owner!', parse_mode='Markdown')
    except:
        bot.reply_to(m, '❌ Invalid ID!', parse_mode='Markdown')

@bot.message_handler(commands=['removeowner'])
def removeowner(m):
    if m.from_user.id != MASTER:
        bot.reply_to(m, '❌ Only master owner can remove owners!', parse_mode='Markdown')
        return
    try:
        parts = m.text.split()
        if len(parts) < 2:
            bot.reply_to(m, '📝 Usage: `/removeowner ID`', parse_mode='Markdown')
            return
        rem = int(parts[1])
        if rem == MASTER:
            bot.reply_to(m, '❌ Cannot remove MASTER owner!', parse_mode='Markdown')
        elif rem in OWNERS:
            OWNERS.remove(rem)
            save_owners(OWNERS)
            bot.reply_to(m, f'🗑️ Owner `{rem}` removed! Total: {len(OWNERS)}', parse_mode='Markdown')
        else:
            bot.reply_to(m, f'⚠️ `{rem}` is not an owner!', parse_mode='Markdown')
    except:
        bot.reply_to(m, '❌ Invalid ID!', parse_mode='Markdown')

@bot.message_handler(commands=['owners'])
def listowners(m):
    if not is_owner(m.from_user.id):
        bot.reply_to(m, '🔒 Only owners can view this!', parse_mode='Markdown')
        return
    txt = '👑 OWNERS LIST 👑\n\n'
    for o in OWNERS:
        if o == MASTER:
            txt += f'⭐ `{o}` (MASTER)\n'
        else:
            txt += f'✅ `{o}`\n'
    txt += f'\n📋 Total: {len(OWNERS)}'
    bot.reply_to(m, txt, parse_mode='Markdown')

@bot.message_handler(commands=['upload'])
def upload(m):
    if not is_owner(m.from_user.id):
        bot.reply_to(m, '🔒 Only owners can upload!', parse_mode='Markdown')
        return
    bot.reply_to(m, '📤 Send me the file (Document/Photo/Video/Audio)', parse_mode='Markdown')

@bot.message_handler(content_types=['document', 'photo', 'video', 'audio'])
def handle_file(m):
    if not is_owner(m.from_user.id):
        bot.reply_to(m, '🔒 Only owners can upload!', parse_mode='Markdown')
        return
    
    global FILE_ID
    file_name = "Unknown"
    
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
    else:
        bot.reply_to(m, '❌ Unsupported file type!', parse_mode='Markdown')
        return
    
    save_file(FILE_ID)
    botname = bot.get_me().username
    
    bot.reply_to(
        m,
        f'✅ **FILE SET SUCCESSFULLY!**\n\n'
        f'{file_type} `{file_name}`\n\n'
        f'🔗 **Download Link:**\n'
        f'`https://t.me/{botname}?start={SECRET}`\n\n'
        f'⏰ File auto-delete: 1 HOUR\n'
        f'📢 Users must join channel first!',
        parse_mode='Markdown'
    )
    
    print(f"✅ File set: {file_name} - ID: {FILE_ID[:30]}...")

@bot.message_handler(commands=['showfile'])
def showfile(m):
    if not is_owner(m.from_user.id):
        return
    if FILE_ID:
        try:
            bot.send_document(m.chat.id, FILE_ID, caption='📁 Current file in bot')
        except Exception as e:
            bot.reply_to(m, f'❌ Error: {e}\n\nFile ID may be expired. Please re-upload.', parse_mode='Markdown')
    else:
        bot.reply_to(m, '❌ No file set! Use /upload', parse_mode='Markdown')

@bot.message_handler(commands=['removefile'])
def removefile(m):
    if not is_owner(m.from_user.id):
        return
    global FILE_ID
    FILE_ID = None
    save_file(None)
    bot.reply_to(m, '🗑️ File removed!', parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status(m):
    if not is_owner(m.from_user.id):
        return
    status_text = '✅ SET' if FILE_ID else '❌ NOT SET'
    bot.reply_to(
        m,
        f'📊 **BOT STATUS**\n\n'
        f'📁 File: {status_text}\n'
        f'👑 Owners: {len(OWNERS)}\n'
        f'⭐ Master: {MASTER}\n'
        f'⏰ Auto-delete: 1 Hour\n'
        f'🔗 Link: `https://t.me/{bot.get_me().username}?start={SECRET}`',
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['ping'])
def ping(m):
    bot.reply_to(m, '🏓 Pong! Bot is alive', parse_mode='Markdown')

# ========== USER COMMANDS ==========

@bot.message_handler(commands=['start'])
def start(m):
    print(f"DEBUG: User {m.from_user.id} - {m.text}")
    
    if not FILE_ID:
        bot.reply_to(m, '❌ No file available! Contact owner.', parse_mode='Markdown')
        return
    
    parts = m.text.split()
    
    # Check if user came from correct link
    if len(parts) > 1 and parts[1] == SECRET:
        # User clicked correct link - send file
        try:
            # Send warning
            bot.send_message(
                m.chat.id,
                '⚠️ **WARNING!** ⚠️\n\n'
                '📁 Ye file **1 GHANTA** baad **AUTO-DELETE** ho jayegi!\n\n'
                '💾 **Abhi download kar lo!**\n'
                '📥 Save karke rakh le!\n\n'
                '🔥 RAI CONFIG ☠️',
                parse_mode='Markdown'
            )
            
            # Send file
            file_msg = bot.send_document(
                m.chat.id,
                FILE_ID,
                caption='🔓 **Ye le teri file!**\n\n⏰ 1 ghanta hai tere paas!\n\n😈 RAI CONFIG ☠️',
                parse_mode='Markdown'
            )
            
            # Auto delete after 1 hour
            threading.Thread(target=delete_later, args=(m.chat.id, file_msg.message_id, 3600)).start()
            
            print(f"✅ File sent to user {m.from_user.id}")
            
        except Exception as e:
            bot.reply_to(m, f'❌ Error sending file: {e}\n\nContact owner.', parse_mode='Markdown')
            print(f"❌ Error: {e}")
    
    elif len(parts) > 1:
        bot.reply_to(
            m,
            f'❌ **GALAT LINK!** ❌\n\n'
            f'🔗 Sahi link format: `https://t.me/{bot.get_me().username}?start={SECRET}`',
            parse_mode='Markdown'
        )
    else:
        bot.reply_to(
            m,
            f'🤡 **CHANNEL LINK SE CLICK KAR!** 🤡\n\n'
            f'🔗 Link: `https://t.me/{bot.get_me().username}?start={SECRET}`\n\n'
            f'❌ Direct `/start` se file nahi milegi!',
            parse_mode='Markdown'
        )

print('='*50)
print('🔥 RAI CONFIG BOT ACTIVATED!')
print(f'👑 Master Owner: {MASTER}')
print(f'📁 File: {"SET" if FILE_ID else "NOT SET"}')
print(f'🔗 Secret: {SECRET}')
print(f'🤖 Bot: @{(bot.get_me()).username}')
print('='*50)
bot.infinity_polling()
