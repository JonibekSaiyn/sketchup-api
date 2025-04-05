import logging
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = "7688201855:AAF9IFE8PwgKzIZJuk8tsn-kKNGyaeagBuc"
API_URL = "https://sketchup-api.onrender.com/api/draw"

logging.basicConfig(level=logging.INFO)

# Шаги для ConversationHandler
WIDTH, HEIGHT, DEPTH, SHELVES = range(4)

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Введи ширину шкафа (в мм):")
    return WIDTH

async def get_width(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['width'] = int(update.message.text)
    await update.message.reply_text("Теперь высоту шкафа (в мм):")
    return HEIGHT

async def get_height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['height'] = int(update.message.text)
    await update.message.reply_text("Теперь глубину шкафа (в мм):")
    return DEPTH

async def get_depth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['depth'] = int(update.message.text)
    await update.message.reply_text("Сколько полок?")
    return SHELVES

async def get_shelves(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['shelves'] = int(update.message.text)
    
    # Отправляем запрос на API
    payload = context.user_data
    response = requests.post(API_URL, json=payload)
    data = response.json()

    if "image_path" in data:
        await update.message.reply_text("Готово! Но картинка пока локальная. Скоро подключим загрузку.")
    else:
        await update.message.reply_text("Ошибка при создании чертежа.")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено.")
    return ConversationHandler.END

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WIDTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_width)],
            HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_height)],
            DEPTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_depth)],
            SHELVES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_shelves)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv_handler)
    print("Бот запущен!")
    app.run_polling()
