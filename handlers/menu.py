from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

async def menu_principal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botoes = [
        ['/cadastrar'],
        ['/cadastrar_receita'],
        ['/fazer_lista'],
        ['/excluir']
    ]
    reply_markup = ReplyKeyboardMarkup(botoes, resize_keyboard=True)
    await update.message.reply_text(
        "📋 Menu principal:\nEscolha uma opção abaixo:",
        reply_markup=reply_markup
    )