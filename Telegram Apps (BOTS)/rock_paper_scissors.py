from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
import random
import logging
import os

BOT_TOKEN = os.getenv("TELEGRAM")
load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GAMES = {}  # {chat_id: {"player1": id, "player2": id, "move1": None, "move2": None}}

CHOICES = ["🪨 Rock", "📄 Paper", "✂️ Scissors"]

def winner(m1, m2):
    if m1 == m2:
        return "🔁 Draw!"
    if (m1 == "Rock" and m2 == "Scissors") or \
       (m1 == "Scissors" and m2 == "Paper") or \
       (m1 == "Paper" and m2 == "Rock"):
        return "Player 1 wins!"
    return "Player 2 wins!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🎮 Play vs Bot", callback_data="bot")],
        [InlineKeyboardButton("👥 Play 2 Players", callback_data="2p")]
    ]
    await update.message.reply_text("Choose game mode:", reply_markup=InlineKeyboardMarkup(kb))

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    user_id = query.from_user.id

    await query.answer()

    if data == "bot":
        kb = [[InlineKeyboardButton(c, callback_data=f"bot_{c.split()[1]}")] for c in CHOICES]
        await query.edit_message_text("Choose your move:", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("bot_"):
        move = data.split("_")[1]
        bot_move = random.choice(["Rock", "Paper", "Scissors"])

        result = winner(move, bot_move)
        await query.edit_message_text(
            f"👤 You: {move}\n🤖 Bot: {bot_move}\n\n🏆 Result: {result}"
        )

    elif data == "2p":
        GAMES[chat_id] = {"player1": user_id, "player2": None, "move1": None, "move2": None}
        await query.edit_message_text("Waiting for Player 2… Tell a friend to press 👉 /join")

    elif data in ["Rock", "Paper", "Scissors"]:
        game = GAMES.get(chat_id)
        if not game:
            return

        if user_id == game["player1"]:
            game["move1"] = data
        elif user_id == game["player2"]:
            game["move2"] = data

        if game["move1"] and game["move2"]:
            res = winner(game["move1"], game["move2"])
            await query.edit_message_text(
                f"Player1: {game['move1']}\nPlayer2: {game['move2']}\n\n🏆 {res}"
            )
            del GAMES[chat_id]

async def join(update: Update, context):
    chat_id = update.message.chat_id
    game = GAMES.get(chat_id)

    if not game:
        return await update.message.reply_text("❌ No active game.")

    if game["player2"] is None:
        game["player2"] = update.message.from_user.id
        kb = [[InlineKeyboardButton(c, callback_data=c.split()[1])] for c in CHOICES]
        await update.message.reply_text("🎯 Players ready!\nChoose your move:", reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text("❌ Game is full.")

app = ApplicationBuilder().token("BOT_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("join", join))
app.add_handler(CallbackQueryHandler(buttons))
app.run_polling()
