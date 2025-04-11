
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random
import os

TOKEN = os.getenv("BOT_TOKEN")

phrases_derzko = [
    "Ты не обязана быть удобной. Ты обязана быть собой.",
    "Ты не милашка — ты Пожар. Жги.",
    "Говоришь дерзко, выглядишь мощно, действуешь громко.",
]

phrases_brat = [
    "Бро, ты справишься. Даже если всё пиздец.",
    "Мы не сдаёмся. Мы просто передохнули. Погнали дальше.",
    "Ты не стекло. Ты бетон с душой.",
]

phrases_mat = [
    "Вставай, блядь. Этот день сам себя не разъебёт.",
    "Ты не проёб, ты перезагрузка. Жми.",
    "Пошли всех нахуй и делай своё. Потому что МОЖЕШЬ.",
]

phrases_all = phrases_derzko + phrases_brat + phrases_mat

keyboard_start = [["Дай смелость"]]
keyboard_styles = [["Дерзко", "По-братски", "С матом"], ["Рандом"]]

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = "waiting_for_dare"
    await update.message.reply_text(
        "Привет, Пожарик. Готова к пинку? Нажми «Дай смелость».",
        reply_markup=ReplyKeyboardMarkup(keyboard_start, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "Дай смелость":
        user_states[user_id] = "choosing_style"
        await update.message.reply_text(
            "Выбери, в каком стиле тебя сегодня разбудить.",
            reply_markup=ReplyKeyboardMarkup(keyboard_styles, resize_keyboard=True)
        )
        return

    if user_states.get(user_id) == "choosing_style":
        if text == "Дерзко":
            await update.message.reply_text(random.choice(phrases_derzko))
        elif text == "По-братски":
            await update.message.reply_text(random.choice(phrases_brat))
        elif text == "С матом":
            await update.message.reply_text(random.choice(phrases_mat))
        elif text == "Рандом":
            await update.message.reply_text(random.choice(phrases_all))
        else:
            await update.message.reply_text("Выбери стиль кнопкой.")
    else:
        await update.message.reply_text("Нажми «Дай смелость», чтобы начать.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
