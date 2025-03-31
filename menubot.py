import os
import logging
import requests
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Lấy token từ biến môi trường
TOKEN = os.getenv("TOKEN")

# Cấu hình logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Hàm lấy số followers của TikTok
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

# Hàm xử lý lệnh /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🔹 Gửi link TikTok để kiểm tra số followers!")

# Hàm xử lý kiểm tra followers
async def check_followers(update: Update, context: CallbackContext) -> None:
    profile_url = update.message.text.strip()
    if "tiktok.com/@" not in profile_url:
        await update.message.reply_text("❌ Link không hợp lệ! Hãy gửi link TikTok hợp lệ.")
    else:
        await update.message.reply_text("🔍 Đang kiểm tra, vui lòng chờ...")
        followers = get_tiktok_followers(profile_url)
        await update.message.reply_text(f"👤 Tài khoản có {followers} followers.")

# Hàm hiển thị menu chức năng
async def menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Check Follow TikTok", callback_data="check_follow")],
        [InlineKeyboardButton("Chức năng 2", callback_data="func2")],
        [InlineKeyboardButton("Chức năng 3", callback_data="func3")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔹 Chọn chức năng:", reply_markup=reply_markup)

# Khởi tạo bot Telegram
def main():
    app = Application.builder().token(TOKEN).build()

    # Thêm các lệnh vào bot
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_followers))

    # Chạy bot
    app.run_polling()

if __name__ == "__main__":
    main()
