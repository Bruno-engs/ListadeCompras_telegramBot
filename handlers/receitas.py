from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from utils.persistencia import carregar_json, salvar_json

RECEITA_NOME, RECEITA_INGREDIENTE, RECEITA_QTD, RECEITA_CONFIRMA = range(3, 7)

async def cadastrar_receita(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['receita_temp'] = {'nome': '', 'ingredientes': []}
    ingredientes = carregar_json('data/ingredientes.json')
    if not ingredientes:
        await update.message.reply_text("⚠️ Cadastre ingredientes antes.")
        return ConversationHandler.END
    context.user_data['todos_ingredientes'] = ingredientes
    await update.message.reply_text("🍽️ Qual o nome da receita?")
    return RECEITA_NOME

async def receita_nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome = update.message.text
    context.user_data['receita_temp']['nome'] = nome
    ingredientes = context.user_data['todos_ingredientes']
    keyboard = [[f"{i['ingrediente']} ({i['unidade']})"] for i in ingredientes]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("📝 Escolha um ingrediente:", reply_markup=markup)
    return RECEITA_INGREDIENTE

async def receita_ingrediente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    escolha = update.message.text
    todos = context.user_data['todos_ingredientes']
    match = next((i for i in todos if f"{i['ingrediente']} ({i['unidade']})" == escolha), None)
    if not match:
        await update.message.reply_text("❌ Ingrediente inválido. Tente novamente.")
        keyboard = [[f"{i['ingrediente']} ({i['unidade']})"] for i in todos]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("📝 Escolha um ingrediente:", reply_markup=markup)
        return RECEITA_INGREDIENTE

    context.user_data['current_ing'] = match
    await update.message.reply_text(f"🔢 Qual a quantidade de {match['ingrediente']} ({match['unidade']})?")
    return RECEITA_QTD

async def receita_qtd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    qtd = update.message.text
    try:
        qtd = float(qtd.replace(',', '.'))
    except ValueError:
        await update.message.reply_text("❌ Quantidade inválida. Digite um número.")
        return RECEITA_QTD

    ing = context.user_data['current_ing']
    context.user_data['receita_temp']['ingredientes'].append({
        'ingrediente': ing['ingrediente'],
        'quantidade': qtd,
        'unidade': ing['unidade']
    })
    reply_markup = ReplyKeyboardMarkup([['Sim', 'Não']], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("✅ Deseja adicionar outro ingrediente?", reply_markup=reply_markup)
    return RECEITA_CONFIRMA

async def confirmar_receita_loop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resp = update.message.text.lower()
    if resp == 'sim':
        ingredientes = context.user_data['todos_ingredientes']
        keyboard = [[f"{i['ingrediente']} ({i['unidade']})"] for i in ingredientes]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("📝 Escolha um ingrediente:", reply_markup=markup)
        return RECEITA_INGREDIENTE

    receita = context.user_data['receita_temp']
    todas = carregar_json('data/receitas.json')
    todas.append(receita)
    salvar_json('data/receitas.json', todas)

    resumo = "\n".join(
        f"• {i['ingrediente']}: {i['quantidade']} {i['unidade']}"
        for i in receita['ingredientes']
    )
    await update.message.reply_text(
        f"✅ Receita '{receita['nome']}' cadastrada!\n\nIngredientes:\n{resumo}"
    )
    from handlers.menu import menu_principal
    await update.message.reply_text("🔙 Voltando ao menu principal...")
    await menu_principal(update, context)
    return ConversationHandler.END

conv_rec = ConversationHandler(
    entry_points=[CommandHandler('cadastrar_receita', cadastrar_receita)],
    states={
        RECEITA_NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receita_nome)],
        RECEITA_INGREDIENTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receita_ingrediente)],
        RECEITA_QTD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receita_qtd)],
        RECEITA_CONFIRMA: [
            MessageHandler(
                filters.Regex(r'^(Sim|Não|sim|não)$'), confirmar_receita_loop
            )
        ],
    },
    fallbacks=[],
    allow_reentry=True
)