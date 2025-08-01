from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from utils.persistencia import carregar_json, salvar_json
from handlers.menu import menu_principal

EXCLUIR_OPCAO, EXCLUIR_ING, EXCLUIR_REC = range(11, 14)

async def excluir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botoes = [
        ['Excluir ingrediente'],
        ['Excluir receita'],
        ['Menu principal']
    ]
    reply_markup = ReplyKeyboardMarkup(botoes, resize_keyboard=True)
    await update.message.reply_text("🗑️ O que deseja excluir?", reply_markup=reply_markup)
    return EXCLUIR_OPCAO

async def excluir_opcao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    escolha = update.message.text
    if escolha == 'Excluir ingrediente':
        ingredientes = carregar_json('data/ingredientes.json')
        if not ingredientes:
            await update.message.reply_text("⚠️ Nenhum ingrediente cadastrado.")
            return await excluir(update, context)
        context.user_data['ingredientes_excluir'] = ingredientes
        keyboard = [[i['ingrediente']] for i in ingredientes]
        reply = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Selecione o ingrediente para excluir:", reply_markup=reply)
        return EXCLUIR_ING

    elif escolha == 'Excluir receita':
        receitas = carregar_json('data/receitas.json')
        if not receitas:
            await update.message.reply_text("⚠️ Nenhuma receita cadastrada.")
            return await excluir(update, context)
        context.user_data['receitas_excluir'] = receitas
        keyboard = [[r['nome']] for r in receitas]
        reply = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Selecione a receita para excluir:", reply_markup=reply)
        return EXCLUIR_REC

    elif escolha == 'Menu principal':
        await menu_principal(update, context)
        return ConversationHandler.END

    else:
        await update.message.reply_text("❌ Opção inválida. Tente novamente.")
        return EXCLUIR_OPCAO

async def excluir_ingrediente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome = update.message.text
    ingredientes = context.user_data.get('ingredientes_excluir', [])
    novos = [i for i in ingredientes if i['ingrediente'] != nome]
    salvar_json('data/ingredientes.json', novos)
    await update.message.reply_text(f"✅ Ingrediente '{nome}' excluído.")
    return await excluir(update, context)

async def excluir_receita(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome = update.message.text
    receitas = context.user_data.get('receitas_excluir', [])
    novas = [r for r in receitas if r['nome'] != nome]
    salvar_json('data/receitas.json', novas)
    await update.message.reply_text(f"✅ Receita '{nome}' excluída.")
    return await excluir(update, context)

conv_excluir = ConversationHandler(
    entry_points=[CommandHandler('excluir', excluir)],
    states={
        EXCLUIR_OPCAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, excluir_opcao)],
        EXCLUIR_ING: [MessageHandler(filters.TEXT & ~filters.COMMAND, excluir_ingrediente)],
        EXCLUIR_REC: [MessageHandler(filters.TEXT & ~filters.COMMAND, excluir_receita)],
    },
    fallbacks=[],
    allow_reentry=True
)