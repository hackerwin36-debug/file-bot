import telebot
import threading
import time
import os
import json
from datetime import datetime

TOKEN = os.environ['TOKEN']
MASTER = int(os.environ['OWNER'])
bot = telebot.TeleBot(TOKEN)

# ========== 🔥 CONFIGURATION ==========
SECRET = 'give_my_file'
CHANNEL_USERNAME = '@RAICONFIGABOUT01'
CHANNEL_LINK = 'https://t.me/+iIZjESjmRPdmNjQ1'
BOT_NAME = '𝗥𝗔𝗜 𝗖𝗢𝗡𝗙𝗜𝗚 ☠️'
# ======================================

FILE_DATA = 'file.json'
OWNER_DATA = 'owners.json'
USERS_DATA = 'users.json'

BANNER = """
╔══════════════════════════════════════════╗
║     🔥 𝗥𝗔𝗜 𝗖𝗢𝗡𝗙𝗜𝗚 ☠️ 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧 🔥     ║
╠══════════════════════════════════════════╣
║      ⚡ AUTO FILE DELIVERY SYSTEM ⚡      ║
║          🎯 1 HOUR AUTO DELETE          ║
║          👑 MULTI OWNER SUPPORT         ║
║          📢 CHANNEL VERIFICATION        ║
║          📣 BROADCAST NOTICE            ║
╚══════════════════════════════════════════╝
"""

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

def load_users():
    try:
        with open(USERS_DATA, 'r') as f:
            return json.load(f).get('users', [])
    except:
        return []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_DATA, 'w') as f:
            json.dump({'users': users}, f)

OWNERS = load_owners()
FILE_ID = load_file()

def is_owner(uid):
    return uid in OWNERS

def is_channel_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

def delete_later(cid, mid, sec):
    time.sleep(sec)
    try:
        bot.delete_message(cid, mid)
    except:
        pass

def get_time():
    return datetime.now().strftime("%I:%M %p")

waiting_broadcast = False

# ========== 📢 BROADCAST FUNCTION ==========

@bot.message_handler(commands=['broadcast'])
def broadcast_cmd(m):
    if not is_owner(m.from_user.id):
        return
    
    global waiting_broadcast
    waiting_broadcast = True
    
    msg = f"""
📢 **BROADCAST NOTICE**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  📝 Send me the message you want to broadcast
┃  ━━━━━━━━━━━━━━━━━
┃  ✅ Supported: Text, Photo, Video, Document
┃  📊 Will be sent to ALL users who used bot
┃  ━━━━━━━━━━━━━━━━━
┃  💡 Send your broadcast message now
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ {BOT_NAME} PREMIUM
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

@bot.message_handler(func=lambda m: hasattr(bot, 'waiting_broadcast') and bot.waiting_broadcast and is_owner(m.from_user.id))
def handle_broadcast(m):
    global waiting_broadcast
    waiting_broadcast = False
    
    users = load_users()
    if not users:
        bot.reply_to(m, '❌ No users found!', parse_mode='Markdown')
        return
    
    sent = 0
    failed = 0
    
    status_msg = bot.reply_to(m, f'📢 Broadcasting to {len(users)} users... ⏳', parse_mode='Markdown')
    
    for user_id in users:
        try:
            if m.text:
                bot.send_message(user_id, f"""
📣 **{BOT_NAME} NOTICE** 📣

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  {m.text}
╰━━━━━━━━━━━━━━━━━━━━━╯

✨ {BOT_NAME} PREMIUM
🕒 {get_time()}
""", parse_mode='Markdown')
            elif m.photo:
                bot.send_photo(user_id, m.photo[-1].file_id, caption=f"📣 {BOT_NAME} NOTICE")
            elif m.document:
                bot.send_document(user_id, m.document.file_id, caption=f"📣 {BOT_NAME} NOTICE")
            sent += 1
        except:
            failed += 1
        time.sleep(0.05)
    
    bot.edit_message_text(
        f"""
✅ **BROADCAST COMPLETED!**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  ✅ Sent: `{sent}`
┃  ❌ Failed: `{failed}`
┃  📋 Total: `{len(users)}`
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ {BOT_NAME} PREMIUM
""",
        status_msg.message_id,
        status_msg.chat.id,
        parse_mode='Markdown'
    )

# ========== 👑 OWNER HELP ==========

@bot.message_handler(commands=['help'])
def help_command(m):
    if not is_owner(m.from_user.id):
        return
    
    users_count = len(load_users())
    msg = f"""
📚 **{BOT_NAME} - OWNER HELP CENTER** 📚

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  👑 **OWNER COMMANDS** 👑
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┃  
┃  🔹 `/upload` - Set/change file in bot
┃  🔹 `/showfile` - View current file
┃  🔹 `/removefile` - Delete file from bot
┃  🔹 `/status` - Check bot status
┃  🔹 `/broadcast` - Send notice to ALL users
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┃  👥 **OWNER MANAGEMENT**
┃  🔹 `/addowner ID` - Add new owner
┃  🔹 `/removeowner ID` - Remove owner
┃  🔹 `/owners` - List all owners
┃  🔹 `/myid` - Get your Telegram ID
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┃  ℹ️ **GENERAL**
┃  🔹 `/help` - Show this menu
┃  🔹 `/ping` - Check bot alive
┃  🔹 `/start` - Welcome message
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✨ {BOT_NAME} PREMIUM
🕒 `{get_time()}`
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

# ========== 👑 OWNER START COMMAND (Jaisa chal raha hai) ==========

@bot.message_handler(commands=['start'])
def start_cmd(m):
    # Agar owner hai toh purana welcome message dikhao
    if is_owner(m.from_user.id):
        if not FILE_ID:
            msg = f"""
✨ **WELCOME TO {BOT_NAME}** ✨

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  🔥 **BOT STATUS** 🔥
┃  ━━━━━━━━━━━━━━━━━
┃  📁 File: `❌ NOT SET`
┃  👑 Mode: `PREMIUM`
┃  ⏰ Auto-Delete: `1 HOUR`
┃  📢 Channel: `{CHANNEL_USERNAME}`
╰━━━━━━━━━━━━━━━━━━━━━╯

💫 **Contact Owner:** @RAICONFIGABOUT01
📚 Type `/help` for commands
🕒 `{get_time()}`
"""
        else:
            msg = f"""
✨ **WELCOME TO {BOT_NAME}** ✨

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  🟢 **BOT ONLINE** 🟢
┃  ━━━━━━━━━━━━━━━━━
┃  📁 File: `✅ READY`
┃  👑 Mode: `PREMIUM`
┃  ⏰ Auto-Delete: `1 HOUR`
┃  📢 Channel: `{CHANNEL_USERNAME}`
┃  📊 Users: `{len(load_users())}`
╰━━━━━━━━━━━━━━━━━━━━━╯

💫 Use `/help` for owner commands
🕒 `{get_time()}`
"""
        bot.reply_to(m, msg, parse_mode='Markdown')
        return
    
    # ========== USER START COMMAND (Sirf channel join ka option) ==========
    save_user(m.from_user.id)
    
    msg = f"""
🔥 **{BOT_NAME}** 🔥

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  📢 **JOIN OUR CHANNEL FIRST** 📢
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┃  
┃  👇 **CLICK HERE TO JOIN**
┃  `{CHANNEL_LINK}`
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┃  
┃  ✅ Channel join karne ke baad
┃  🔗 Channel me diye link se click karo
┃  📁 File automatically mil jayegi!
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┃  ⚠️ **NOTE:**
┃  ┣ ❌ Direct `/start` se file nahi milegi
┃  ┣ ✅ Sirf channel link se click karne par
┃  ┗ ⏰ File 1 ghante baad delete ho jayegi
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

✨ {BOT_NAME} PREMIUM
👑 Owner: @RAICONFIGABOUT01
🕒 `{get_time()}`
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

# ========== USER FILE GET (Channel link se) ==========

@bot.message_handler(func=lambda m: m.text and m.text.startswith('/start') and len(m.text.split()) > 1 and m.text.split()[1] == SECRET)
def user_file_request(m):
    # Ye sirf tab trigger hoga jab user channel link se click karega
    # Format: /start give_my_file
    
    save_user(m.from_user.id)
    
    if not FILE_ID:
        bot.reply_to(m, '❌ No file available! Contact owner.', parse_mode='Markdown')
        return
    
    # Check if user joined channel
    if not is_channel_member(m.from_user.id):
        msg = f"""
🔒 **CHANNEL VERIFICATION REQUIRED** 🔒

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  📢 You haven't joined our channel yet!
┃  ━━━━━━━━━━━━━━━━━
┃  👇 **JOIN HERE FIRST**
┃  `{CHANNEL_LINK}`
┃  ━━━━━━━━━━━━━━━━━
┃  ✅ After joining, click link again!
┃  ⚠️ Without joining → NO FILE
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ {BOT_NAME} PREMIUM
"""
        bot.reply_to(m, msg, parse_mode='Markdown')
        return
    
    # User verified - send file
    bot.send_message(
        m.chat.id,
        f"""
✅ **VERIFICATION SUCCESSFUL!** ✅

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  ⚠️ **AUTO-DELETE WARNING**
┃  ━━━━━━━━━━━━━━━━━
┃  📁 This file will be deleted in
┃  ⏰ **1 HOUR** from now!
┃  ━━━━━━━━━━━━━━━━━
┃  💾 **SAVE IT NOW!**
┃  📥 Download immediately
┃  ━━━━━━━━━━━━━━━━━
┃  🔥 {BOT_NAME}
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ Enjoy! 🕒 `{get_time()}`
""",
        parse_mode='Markdown'
    )
    
    f = bot.send_document(
        m.chat.id,
        FILE_ID,
        caption=f"""
🔓 **FILE DELIVERED**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  ⏰ **Expires in:** `1 HOUR`
┃  📢 **Channel:** {CHANNEL_USERNAME}
┃  🔥 {BOT_NAME}
╰━━━━━━━━━━━━━━━━━━━━━╯
""",
        parse_mode='Markdown'
    )
    
    threading.Thread(target=delete_later, args=(m.chat.id, f.message_id, 3600)).start()

# ========== OTHER OWNER COMMANDS ==========

@bot.message_handler(commands=['myid'])
def myid(m):
    if not is_owner(m.from_user.id):
        return
    msg = f"""
👤 **YOUR IDENTITY**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  🆔 **ID:** `{m.from_user.id}`
┃  📛 **NAME:** `{m.from_user.first_name}`
┃  👑 **ROLE:** `OWNER`
╰━━━━━━━━━━━━━━━━━━━━━╯
🕒 `{get_time()}`
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

@bot.message_handler(commands=['addowner'])
def addowner(m):
    if m.from_user.id != MASTER:
        return
    try:
        parts = m.text.split()
        if len(parts) < 2:
            bot.reply_to(m, 'Usage: /addowner ID', parse_mode='Markdown')
            return
        new = int(parts[1])
        if new not in OWNERS:
            OWNERS.append(new)
            save_owners(OWNERS)
            bot.reply_to(m, f'✅ Owner {new} added! Total: {len(OWNERS)}', parse_mode='Markdown')
        else:
            bot.reply_to(m, f'⚠️ {new} is already an owner!', parse_mode='Markdown')
    except:
        bot.reply_to(m, '❌ Invalid ID!', parse_mode='Markdown')

@bot.message_handler(commands=['removeowner'])
def removeowner(m):
    if m.from_user.id != MASTER:
        return
    try:
        parts = m.text.split()
        if len(parts) < 2:
            bot.reply_to(m, 'Usage: /removeowner ID', parse_mode='Markdown')
            return
        rem = int(parts[1])
        if rem == MASTER:
            bot.reply_to(m, '❌ Cannot remove MASTER owner!', parse_mode='Markdown')
        elif rem in OWNERS:
            OWNERS.remove(rem)
            save_owners(OWNERS)
            bot.reply_to(m, f'🗑️ Owner {rem} removed! Total: {len(OWNERS)}', parse_mode='Markdown')
        else:
            bot.reply_to(m, f'⚠️ {rem} is not an owner!', parse_mode='Markdown')
    except:
        bot.reply_to(m, '❌ Invalid ID!', parse_mode='Markdown')

@bot.message_handler(commands=['owners'])
def listowners(m):
    if not is_owner(m.from_user.id):
        return
    txt = f"👑 OWNERS ({len(OWNERS)}):\n"
    for o in OWNERS:
        txt += f"⭐ {o} (MASTER)\n" if o == MASTER else f"✅ {o}\n"
    bot.reply_to(m, txt, parse_mode='Markdown')

@bot.message_handler(commands=['upload'])
def upload(m):
    if not is_owner(m.from_user.id):
        return
    bot.reply_to(m, '📤 Send me the file to set in bot', parse_mode='Markdown')

@bot.message_handler(content_types=['document', 'photo', 'video', 'audio'])
def handle_file(m):
    if not is_owner(m.from_user.id):
        return
    
    global FILE_ID
    file_name = "Unknown"
    
    if m.document:
        FILE_ID = m.document.file_id
        file_name = m.document.file_name
    elif m.photo:
        FILE_ID = m.photo[-1].file_id
        file_name = "Photo.jpg"
    elif m.video:
        FILE_ID = m.video.file_id
        file_name = m.video.file_name or "Video.mp4"
    elif m.audio:
        FILE_ID = m.audio.file_id
        file_name = m.audio.file_name or "Audio.mp3"
    
    save_file(FILE_ID)
    botname = bot.get_me().username
    
    msg = f"""
✅ **FILE SET!**

📄 {file_name}
🔗 `https://t.me/{botname}?start={SECRET}`

📢 Users must join {CHANNEL_USERNAME} first!
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

@bot.message_handler(commands=['showfile'])
def showfile(m):
    if not is_owner(m.from_user.id):
        return
    if FILE_ID:
        bot.send_document(m.chat.id, FILE_ID, caption='📁 Current file in bot')
    else:
        bot.reply_to(m, '❌ No file set! Use /upload')

@bot.message_handler(commands=['removefile'])
def removefile(m):
    if not is_owner(m.from_user.id):
        return
    global FILE_ID
    FILE_ID = None
    save_file(None)
    bot.reply_to(m, '🗑️ File removed!')

@bot.message_handler(commands=['status'])
def status(m):
    if not is_owner(m.from_user.id):
        return
    users_count = len(load_users())
    msg = f"""
📊 **BOT STATUS**

📁 File: {"✅ SET" if FILE_ID else "❌ NOT SET"}
👑 Owners: {len(OWNERS)}
📢 Channel: {CHANNEL_USERNAME}
⏰ Auto-Delete: 1 HOUR
📊 Users: {users_count}
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

@bot.message_handler(commands=['ping'])
def ping(m):
    if not is_owner(m.from_user.id):
        return
    bot.reply_to(m, '🏓 Pong! Bot is alive', parse_mode='Markdown')

print(BANNER)
print(f"🔥 {BOT_NAME} ACTIVATED!")
print(f"👑 Master Owner: {MASTER}")
print(f"📢 Channel: {CHANNEL_USERNAME}")
print(f"📁 File Status: {'SET' if FILE_ID else 'NOT SET'}")
print("="*50)
bot.infinity_polling()
