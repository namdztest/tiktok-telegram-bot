import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# Lấy token từ biến môi trường
TOKEN = os.getenv("TOKEN")

# Cấu hình logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Hàm hiển thị menu
async def menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Chức năng 1", callback_data="func1")],
        [InlineKeyboardButton("Chức năng 2", callback_data="func2")],
        [InlineKeyboardButton("Chức năng 3", callback_data="func3")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔹 Chọn chức năng:", reply_markup=reply_markup)

# Hàm khởi chạy bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("menu", menu))
    app.run_polling()

if __name__ == "__main__":
    main()
