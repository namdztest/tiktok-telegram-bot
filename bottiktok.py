import requests
import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

# Token Telegram (Lấy từ BotFather)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def get_tiktok_followers(profile_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(profile_url, headers=headers)
        if response.status_code == 200:
            html = response.text
            match = re.search(r'(\d+(?:\.\d+)?[KM]?) Followers', html)
            return match.group(1) if match else "Không tìm thấy số followers!"
        return "Lỗi khi truy cập TikTok!"
    except Exception as e:
        return f"Lỗi: {e}"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🔹 Gửi link TikTok để kiểm tra số followers!")

def check_followers(update: Update, context: CallbackContext) -> None:
    profile_url = update.message.text.strip()
    if "tiktok.com/@" not in profile_url:
        update.message.reply_text("❌ Link không hợp lệ! Hãy gửi link TikTok hợp lệ.")
    else:
        update.message.reply_text("🔍 Đang kiểm tra, vui lòng chờ...")
        followers = get_tiktok_followers(profile_url)
        update.message.reply_text(f"👤 Tài khoản có {followers} followers.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_followers))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
