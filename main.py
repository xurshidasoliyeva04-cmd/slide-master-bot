import os
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# 1. RENDER UCHUN "TIRIK SAQLASH" QISMI
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    # Render avtomatik ravishda 10000 yoki 8080 portni kutadi
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.start()

# 2. BOTNING ASOSIY FUNKSIYALARI
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['📊 Slayd Yaratish']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Xush kelibsiz! Kreditlaringiz: 2",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == '📊 Slayd Yaratish':
        await update.message.reply_text("Qanday mavzuda slayd yaratmoqchisiz?")
    else:
        await update.message.reply_text(f"Siz yozdingiz: {text}. Tez orada slayd tayyor bo'ladi!")

# 3. ASOSIY ISHGA TUSHIRISH
if __name__ == '__main__':
    # Render-ni aldash uchun veb-serverni yoqamiz
    keep_alive()
    
    # Telegram botni yoqish (TOKEN-ni Environment-dan oladi)
    token = os.environ.get("BOT_TOKEN")
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot ishga tushdi...")
    application.run_polling()
    
