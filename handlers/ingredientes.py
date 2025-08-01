from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from utils.persistencia import carregar_json, salvar_json

INGREDIENTE, UNIDADE, CONFIRMA = range(3)
UNIDADES_DISPONIVEIS = ['kg', 'un', 'cx', 'g', 'ml']

async def iniciar_cadastro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['cadastros'] = []
    await update.message.reply_text("🍅 Qual o nome do ingrediente?")
    return INGREDIENTE

async def receber_ingrediente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ingrediente = update.message.text
    context.user_data['ingrediente_atual'] = ingrediente
    keyboard = [[u] for u in UNIDADES_DISPONIVEIS]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("📏 Escolha a unidade desse ingrediente:", reply_markup=markup)
    return UNIDADE

async def receber_unidade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ingrediente = context.user_data['ingrediente_atual']
    unidade = update.message.text
    context.user_data['cadastros'].append({
        "ingrediente": ingrediente,
        "unidade": unidade
    })
    reply_markup = ReplyKeyboardMarkup([['Sim', 'Não']], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("✅ Deseja cadastrar outro ingrediente?", reply_markup=reply_markup)
    return CONFIRMA

async def confirmar_loop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() == 'sim':
        await update.message.reply_text("🍅 Qual o nome do próximo ingrediente?")
        return INGREDIENTE

    salvar_json('data/ingredientes.json', context.user_data['cadastros'])

    lista = "\n".join(
        f"• {item['ingrediente']} ({item['unidade']})"
        for item in context.user_data['cadastros']
    )
    await update.message.reply_text(f"📋 Ingredientes cadastrados:\n{lista}")
    from handlers.menu import menu_principal
    await update.message.reply_text("🔙 Voltando ao menu principal...")
    await menu_principal(update, context)
    return ConversationHandler.END

# handlers/ingredientes.py

async def fallback_ingrediente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[u] for u in UNIDADES_DISPONIVEIS]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Opção inválida. Escolha uma unidade:", reply_markup=markup)
    return UNIDADE

conv_ing = ConversationHandler(
    entry_points=[CommandHandler('cadastrar', iniciar_cadastro)],
    states={
        INGREDIENTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_ingrediente)],
        UNIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_unidade)],
        CONFIRMA: [MessageHandler(filters.Regex(r'^(Sim|Não|sim|não)$'), confirmar_loop)],
    },
    fallbacks=[MessageHandler(filters.ALL, fallback_ingrediente)],
    allow_reentry=True
)

conv_ing = ConversationHandler(
    entry_points=[CommandHandler('cadastrar', iniciar_cadastro)],
    states={
        INGREDIENTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_ingrediente)],
        UNIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_unidade)],
        CONFIRMA: [MessageHandler(filters.Regex(r'^(Sim|Não|sim|não)$'), confirmar_loop)],
    },
    fallbacks=[MessageHandler(filters.ALL, fallback_ingrediente)],
    allow_reentry=True
)