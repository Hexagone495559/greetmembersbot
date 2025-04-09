
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)
from datetime import datetime
import pytz
import random
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

def get_time_based_greeting():
    now = datetime.now(pytz.timezone('Asia/Kolkata'))
    hour = now.hour
    day = now.strftime('%A')

    if 5 <= hour < 12:
        greeting = "☀️ 𝐆𝐨𝐨𝐝 𝐌𝐨𝐫𝐧𝐢𝐧𝐠"
    elif 12 <= hour < 17:
        greeting = "🌤️ 𝐆𝐨𝐨𝐝 𝐀𝐟𝐭𝐞𝐫𝐧𝐨𝐨𝐧"
    elif 17 <= hour < 21:
        greeting = "🌇 𝐆𝐨𝐨𝐝 𝐄𝐯𝐞𝐧𝐢𝐧𝐠"
    else:
        greeting = "🌙 𝐆𝐨𝐨𝐝 𝐍𝐢𝐠𝐡𝐭"

    day_msgs = {
        "Monday": "💪 𝐋𝐞𝐭’𝐬 𝐬𝐭𝐚𝐫𝐭 𝐭𝐡𝐞 𝐰𝐞𝐞𝐤 𝐬𝐭𝐫𝐨𝐧𝐠!",
        "Tuesday": "🚀 𝐊𝐞𝐞𝐩 𝐩𝐮𝐬𝐡𝐢𝐧𝐠 𝐚𝐡𝐞𝐚𝐝!",
        "Wednesday": "🐫 𝐌𝐢𝐝-𝐰𝐞𝐞𝐤 𝐯𝐢𝐛𝐞𝐬!",
        "Thursday": "✨ 𝐀𝐥𝐦𝐨𝐬𝐭 𝐭𝐡𝐞 𝐰𝐞𝐞𝐤𝐞𝐧𝐝!",
        "Friday": "🎉 𝐓𝐢𝐦𝐞 𝐭𝐨 𝐞𝐧𝐝 𝐬𝐭𝐫𝐨𝐧𝐠!",
        "Saturday": "🕺 𝐖𝐞𝐞𝐤𝐞𝐧𝐝 𝐦𝐨𝐝𝐞 𝐨𝐧!",
        "Sunday": "☕️ 𝐑𝐞𝐥𝐚𝐱 & 𝐫𝐞𝐜𝐡𝐚𝐫𝐠𝐞!"
    }

    return f"{greeting}! {day_msgs.get(day, '')}"

def get_random_welcome():
    greetings = [
        "✨ 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 {name}! 𝐘𝐨𝐮’𝐫𝐞 𝐚 𝐯𝐢𝐛𝐞 𝐚𝐝𝐝𝐞𝐫!",
        "🌟 𝐇𝐞𝐲 {name}! 𝐋𝐞𝐭'𝐬 𝐠𝐞𝐭 𝐬𝐨𝐜𝐢𝐚𝐥!",
        "🎊 𝐇𝐞𝐥𝐥𝐨 {name}! 𝐍𝐢𝐜𝐞 𝐭𝐨 𝐡𝐚𝐯𝐞 𝐲𝐨𝐮!",
        "❤️ 𝐇𝐞𝐲 {name}, 𝐲𝐨𝐮’𝐫𝐞 𝐥𝐨𝐯𝐞𝐝 𝐡𝐞𝐫𝐞!",
        "☕️ 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 {name}, 𝐭𝐚𝐤𝐞 𝐚 𝐬𝐞𝐚𝐭 𝐚𝐧𝐝 𝐜𝐡𝐢𝐥𝐥!"
    ]
    return random.choice(greetings)

async def welcome_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_members = update.message.new_chat_members
    for member in new_members:
        name = member.full_name
        mention = f"[{name}](tg://user?id={member.id})"
        greeting = get_time_based_greeting()
        welcome_msg = get_random_welcome().format(name=mention)
        full_msg = f"{greeting}\n{welcome_msg}"

        photos = await context.bot.get_user_profile_photos(member.id)
        if photos.total_count > 0:
            file_id = photos.photos[0][-1].file_id
            await context.bot.send_chat_action(update.effective_chat.id, ChatAction.UPLOAD_PHOTO)
            await update.message.reply_photo(photo=file_id, caption=full_msg, parse_mode="Markdown")
        else:
            await update.message.reply_text(full_msg, parse_mode="Markdown")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add me to your group", url="https://t.me/Greetmembersbot?startgroup=true")]
    ])
    msg = (
        "👋 *Hey there! I'm your Welcome Bot!* 🤖\n\n"
        "➕ *Add me to your group and I'll greet every new member with:*\n"
        "🖼️ Profile photo\n"
        "⏰ Time-based greeting\n"
        "💬 Stylish, fun, and positive vibes!\n\n"
        "✨ *Let's make your group awesome together!*"
    )
    await update.message.reply_text(msg, reply_markup=keyboard, parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_user))
    print("Bot is running...")
    app.run_polling()
