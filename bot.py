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

BANNER = """
╔══════════════════════════════════════════╗
║     🔥 𝗥𝗔𝗜 𝗖𝗢𝗡𝗙𝗜𝗚 ☠️ 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧 🔥     ║
╠══════════════════════════════════════════╣
║      ⚡ AUTO FILE DELIVERY SYSTEM ⚡      ║
║          🎯 1 HOUR AUTO DELETE          ║
║          👑 MULTI OWNER SUPPORT         ║
║          📢 CHANNEL VERIFICATION        ║
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

# ========== 📚 HELP COMMAND ==========

@bot.message_handler(commands=['help'])
def help_command(m):
    is_owner_user = is_owner(m.from_user.id)
    
    if is_owner_user:
        msg = f"""
📚 **{BOT_NAME} - HELP CENTER** 📚

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  👑 **OWNER COMMANDS** 👑
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┃  
┃  🔹 `/upload` - Set/change file in bot
┃  🔹 `/showfile` - View current file
┃  🔹 `/removefile` - Delete file from bot
┃  🔹 `/status` - Check bot status
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

📌 **FILE SETUP GUIDE:**
1. Use `/upload` command
2. Send your file (document/photo/video/audio)
3. File automatically sets in bot
4. Share channel link with users

✨ {BOT_NAME} PREMIUM
🕒 `{get_time()}`
"""
    else:
        msg = f"""
📚 **{BOT_NAME} - HOW TO GET FILE** 📚

╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  📢 **STEPS TO GET FILE** 📢
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┃  
┃  ✅ **STEP 1:** Join our channel
┃     👇 {CHANNEL_USERNAME}
┃  
┃  ✅ **STEP 2:** Click channel link
┃     🔗 https://t.me/...?start=give_my_file
┃  
┃  ✅ **STEP 3:** File automatically delivers!
┃     ⏰ Auto-delete in 1 HOUR
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┃  ⚠️ **IMPORTANT NOTES**
┃  ┣ ❌ `/start` won't give you file
┃  ┣ ✅ Only channel link works
┃  ┣ 🔒 Channel join required
┃  ┗ ⏰ Save file before 1 hour
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┃  ℹ️ **COMMANDS YOU CAN USE**
┃  🔹 `/help` - Show this menu
┃  🔹 `/ping` - Check bot status
┃  🔹 `/start` - Welcome message
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

🔗 **CHANNEL LINK:** {CHANNEL_LINK}

✨ {BOT_NAME} PREMIUM
🕒 `{get_time()}`
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def start_cmd(m):
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
📚 Type `/help` for guide
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
╰━━━━━━━━━━━━━━━━━━━━━╯

💫 **Get File:** Channel link pe click karo!
📚 Type `/help` for guide
🕒 `{get_time()}`
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

@bot.message_handler(commands=['myid'])
def myid(m):
    msg = f"""
👤 **YOUR IDENTITY**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  🆔 **ID:** `{m.from_user.id}`
┃  📛 **NAME:** `{m.from_user.first_name}`
┃  👑 **ROLE:** `{"OWNER" if is_owner(m.from_user.id) else "USER"}`
╰━━━━━━━━━━━━━━━━━━━━━╯

💫 Share this ID with @RAICONFIGABOUT01
📚 Type `/help` for guide
🕒 `{get_time()}`
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

@bot.message_handler(commands=['addowner'])
def addowner(m):
    if m.from_user.id != MASTER:
        msg = f"""
❌ **ACCESS DENIED**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  🔒 You are not authorized
┃  👑 Only MASTER OWNER can use this
╰━━━━━━━━━━━━━━━━━━━━━╯
"""
        bot.reply_to(m, msg, parse_mode='Markdown')
        return
    try:
        parts = m.text.split()
        if len(parts) < 2:
            msg = f"""
📝 **ADD OWNER**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  💡 **Usage:** `/addowner ID`
┃  📌 **Example:** `/addowner 123456789`
╰━━━━━━━━━━━━━━━━━━━━━╯
"""
            bot.reply_to(m, msg, parse_mode='Markdown')
            return
        new = int(parts[1])
        if new not in OWNERS:
            OWNERS.append(new)
            save_owners(OWNERS)
            msg = f"""
✅ **OWNER ADDED**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  👑 New Owner: `{new}`
┃  📋 Total Owners: `{len(OWNERS)}`
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ {BOT_NAME} PREMIUM
🕒 `{get_time()}`
"""
        else:
            msg = f"""
⚠️ **ALREADY OWNER**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  👑 `{new}` is already an owner!
╰━━━━━━━━━━━━━━━━━━━━━╯
"""
        bot.reply_to(m, msg, parse_mode='Markdown')
    except:
        msg = f"""
❌ **INVALID ID**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  💡 Use numbers only!
┃  📌 Example: `/addowner 123456789`
╰━━━━━━━━━━━━━━━━━━━━━╯
"""
        bot.reply_to(m, msg, parse_mode='Markdown')

@bot.message_handler(commands=['removeowner'])
def removeowner(m):
    if m.from_user.id != MASTER:
        msg = f"""
❌ **ACCESS DENIED**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  🔒 Only MASTER OWNER can use this
╰━━━━━━━━━━━━━━━━━━━━━╯
"""
        bot.reply_to(m, msg, parse_mode='Markdown')
        return
    try:
        parts = m.text.split()
        if len(parts) < 2:
            msg = f"""
📝 **REMOVE OWNER**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  💡 **Usage:** `/removeowner ID`
┃  📌 **Example:** `/removeowner 123456789`
╰━━━━━━━━━━━━━━━━━━━━━╯
"""
            bot.reply_to(m, msg, parse_mode='Markdown')
            return
        rem = int(parts[1])
        if rem == MASTER:
            msg = f"""
🔥 **CANNOT REMOVE**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  ⭐ MASTER OWNER cannot be removed!
╰━━━━━━━━━━━━━━━━━━━━━╯
"""
        elif rem in OWNERS:
            OWNERS.remove(rem)
            save_owners(OWNERS)
            msg = f"""
🗑️ **OWNER REMOVED**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  👑 Removed: `{rem}`
┃  📋 Total Owners: `{len(OWNERS)}`
╰━━━━━━━━━━━━━━━━━━━━━╯
"""
        else:
            msg = f"""
⚠️ **NOT AN OWNER**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  ❌ `{rem}` is not an owner!
╰━━━━━━━━━━━━━━━━━━━━━╯
"""
        bot.reply_to(m, msg, parse_mode='Markdown')
    except:
        msg = f"""
❌ **INVALID ID**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  💡 Use numbers only!
╰━━━━━━━━━━━━━━━━━━━━━╯
"""
        bot.reply_to(m, msg, parse_mode='Markdown')

@bot.message_handler(commands=['owners'])
def listowners(m):
    if not is_owner(m.from_user.id):
        return
    txt = f"""
👑 **OWNERS LIST** 👑

╭━━━━━━━━━━━━━━━━━━━━━╮
"""
    for o in OWNERS:
        if o == MASTER:
            txt += f"┃  ⭐ `{o}` (MASTER)\n"
        else:
            txt += f"┃  ✅ `{o}`\n"
    txt += f"""┃  ━━━━━━━━━━━━━━━━━
┃  📋 **Total:** `{len(OWNERS)}`
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ {BOT_NAME} PREMIUM
🕒 `{get_time()}`
"""
    bot.reply_to(m, txt, parse_mode='Markdown')

@bot.message_handler(commands=['upload'])
def upload(m):
    if not is_owner(m.from_user.id):
        msg = f"""
❌ **ACCESS DENIED**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  🔒 Only owners can upload files!
╰━━━━━━━━━━━━━━━━━━━━━╯
"""
        bot.reply_to(m, msg, parse_mode='Markdown')
        return
    msg = f"""
📤 **FILE UPLOAD**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  📁 Send me your file now!
┃  ━━━━━━━━━━━━━━━━━
┃  ✅ Supported Formats:
┃  ┣ 📄 Document
┃  ┣ 🖼️ Photo
┃  ┣ 🎬 Video
┃  ┗ 🎵 Audio
┃  ━━━━━━━━━━━━━━━━━
┃  ⏰ Auto-Delete: `1 HOUR`
┃  📢 Channel: `{CHANNEL_USERNAME}`
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ {BOT_NAME} PREMIUM
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

@bot.message_handler(content_types=['document', 'photo', 'video', 'audio'])
def handle_file(m):
    if not is_owner(m.from_user.id):
        return
    
    global FILE_ID
    file_name = "Unknown"
    file_emoji = "📄"
    
    if m.document:
        FILE_ID = m.document.file_id
        file_name = m.document.file_name
        file_emoji = "📄"
    elif m.photo:
        FILE_ID = m.photo[-1].file_id
        file_name = "Photo.jpg"
        file_emoji = "🖼️"
    elif m.video:
        FILE_ID = m.video.file_id
        file_name = m.video.file_name or "Video.mp4"
        file_emoji = "🎬"
    elif m.audio:
        FILE_ID = m.audio.file_id
        file_name = m.audio.file_name or "Audio.mp3"
        file_emoji = "🎵"
    
    save_file(FILE_ID)
    botname = bot.get_me().username
    
    msg = f"""
✅ **FILE SET SUCCESSFULLY!**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  {file_emoji} **FILE DETAILS**
┃  ━━━━━━━━━━━━━━━━━
┃  📛 Name: `{file_name}`
┃  🆔 ID: `{FILE_ID[:25]}...`
┃  ━━━━━━━━━━━━━━━━━
┃  🔗 **DOWNLOAD LINK**
┃  `https://t.me/{botname}?start={SECRET}`
┃  ━━━━━━━━━━━━━━━━━
┃  📢 **REQUIREMENTS**
┃  ┣ ✅ Join: `{CHANNEL_USERNAME}`
┃  ┗ ⏰ Auto-Delete: `1 HOUR`
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ {BOT_NAME} PREMIUM
🕒 `{get_time()}`
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

@bot.message_handler(commands=['showfile'])
def showfile(m):
    if not is_owner(m.from_user.id):
        return
    if FILE_ID:
        bot.send_document(m.chat.id, FILE_ID, caption=f"""
📁 **CURRENT FILE**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  ✅ This is what users get!
┃  🔗 Channel: `{CHANNEL_USERNAME}`
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ {BOT_NAME} PREMIUM
""", parse_mode='Markdown')
    else:
        msg = f"""
❌ **NO FILE SET**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  💡 Use `/upload` to set a file
╰━━━━━━━━━━━━━━━━━━━━━╯
"""
        bot.reply_to(m, msg, parse_mode='Markdown')

@bot.message_handler(commands=['removefile'])
def removefile(m):
    if not is_owner(m.from_user.id):
        return
    global FILE_ID
    FILE_ID = None
    save_file(None)
    msg = f"""
🗑️ **FILE REMOVED**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  ❌ File has been deleted from bot
┃  💡 Use `/upload` to set new file
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ {BOT_NAME} PREMIUM
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status(m):
    if not is_owner(m.from_user.id):
        return
    status_emoji = '🟢' if FILE_ID else '🔴'
    status_text = 'ONLINE' if FILE_ID else 'STANDBY'
    msg = f"""
📊 **BOT STATUS PANEL**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  {status_emoji} **STATUS:** `{status_text}`
┃  📁 **FILE:** `{"✅ SET" if FILE_ID else "❌ NOT SET"}`
┃  👑 **OWNERS:** `{len(OWNERS)}`
┃  📢 **CHANNEL:** `{CHANNEL_USERNAME}`
┃  ⏰ **AUTO-DELETE:** `1 HOUR`
┃  🔄 **UPTIME:** `24/7`
┃  🎯 **MODE:** `PREMIUM`
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ {BOT_NAME} PREMIUM
🕒 `{get_time()}`
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

# ========== USER COMMANDS ==========

@bot.message_handler(commands=['start'])
def user_start(m):
    if not FILE_ID:
        msg = f"""
✨ **{BOT_NAME}** ✨

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  🔴 **MAINTENANCE MODE**
┃  ━━━━━━━━━━━━━━━━━
┃  📢 No file available yet
┃  👑 Contact: @RAICONFIGABOUT01
╰━━━━━━━━━━━━━━━━━━━━━╯
"""
        bot.reply_to(m, msg, parse_mode='Markdown')
        return
    
    parts = m.text.split()
    
    if len(parts) < 2 or parts[1] != SECRET:
        msg = f"""
🤡 **INVALID ACCESS**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  🔗 Use channel link only!
┃  📢 Join: `{CHANNEL_USERNAME}`
┃  ━━━━━━━━━━━━━━━━━
┃  ❌ Direct `/start` won't work
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ {BOT_NAME} PREMIUM
"""
        bot.reply_to(m, msg, parse_mode='Markdown')
        return
    
    if not is_channel_member(m.from_user.id):
        msg = f"""
🔒 **CHANNEL VERIFICATION REQUIRED**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  📢 **JOIN OUR CHANNEL FIRST**
┃  ━━━━━━━━━━━━━━━━━
┃  👇 **CLICK HERE TO JOIN**
┃  `{CHANNEL_LINK}`
┃  ━━━━━━━━━━━━━━━━━
┃  ✅ After joining, click link again!
┃  ⚠️ Without joining → NO FILE
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ {BOT_NAME} PREMIUM
"""
        bot.reply_to(m, msg, parse_mode='Markdown')
        return
    
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

@bot.message_handler(commands=['ping'])
def ping(m):
    msg = f"""
🏓 **PONG!**

╭━━━━━━━━━━━━━━━━━━━━━╮
┃  🟢 **STATUS:** `ONLINE`
┃  ⚡ **RESPONSE:** `ACTIVE`
┃  🔥 **MODE:** `PREMIUM`
┃  📢 **CHANNEL:** {CHANNEL_USERNAME}
┃  ⏰ **AUTO-DELETE:** `1 HOUR`
╰━━━━━━━━━━━━━━━━━━━━━╯
✨ {BOT_NAME}
🕒 `{get_time()}`
"""
    bot.reply_to(m, msg, parse_mode='Markdown')

print(BANNER)
print(f"🔥 {BOT_NAME} ACTIVATED!")
print(f"👑 Master Owner: {MASTER}")
print(f"📢 Channel: {CHANNEL_USERNAME}")
print(f"📁 File Status: {'SET' if FILE_ID else 'NOT SET'}")
print("="*50)
bot.infinity_polling()
