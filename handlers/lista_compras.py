from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from handlers.menu import menu_principal
from utils.persistencia import carregar_json

LISTA_OPCAO, LISTA_INGREDIENTE, LISTA_QTD, LISTA_RECEITA = range(7, 11)

async def iniciar_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['lista_compra'] = context.user_data.get('lista_compra', [])
    keyboard = [
        ['Adc. Ingrediente'],
        ['Adc. Receita'],
        ['Finalizar lista de compras']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🛒 O que deseja acrescentar a sua lista?", reply_markup=reply_markup)
    return LISTA_OPCAO

async def lista_opcao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    escolha = update.message.text

    if escolha == 'Adc. Ingrediente':
        ingredientes = carregar_json('data/ingredientes.json')
        if not ingredientes:
            await update.message.reply_text("⚠️ Cadastre ingredientes antes.")
            return LISTA_OPCAO
        context.user_data['todos_para_lista'] = ingredientes
        keyboard = [[f"{i['ingrediente']} ({i['unidade']})"] for i in ingredientes]
        reply = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("📝 Escolha um ingrediente:", reply_markup=reply)
        return LISTA_INGREDIENTE

    elif escolha == 'Adc. Receita':
        receitas = carregar_json('data/receitas.json')
        if not receitas:
            await update.message.reply_text("⚠️ Cadastre receitas antes.")
            return LISTA_OPCAO
        context.user_data['todas_receitas'] = receitas
        keyboard = [[r['nome']] for r in receitas]
        reply = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("📖 Escolha uma receita:", reply_markup=reply)
        return LISTA_RECEITA

    elif escolha == 'Finalizar lista de compras':
        lista = context.user_data.get('lista_compra', [])
        if not lista:
            await update.message.reply_text("🛒 Sua lista está vazia.")
        else:
            itens = "\n".join(f"• {x['ingrediente']}: {x['quantidade']} {x['unidade']}" for x in lista)
            await update.message.reply_text(f"🛒 Lista final de compras:\n{itens}")
        await update.message.reply_text("🔙 Voltando ao menu principal...")
        await menu_principal(update, context)
        return ConversationHandler.END

    else:
        await update.message.reply_text("❌ Opção inválida. Tente novamente.")
        return LISTA_OPCAO

async def lista_receita(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome = update.message.text
    receitas = context.user_data.get('todas_receitas', [])
    match = next((r for r in receitas if r['nome'] == nome), None)
    if not match:
        await update.message.reply_text("❌ Receita inválida. Tente novamente.")
        return LISTA_RECEITA

    lista = context.user_data['lista_compra']

    # para cada ingrediente da receita, soma ou adiciona
    for ing in match['ingredientes']:
        existente = next((x for x in lista if x['ingrediente'] == ing['ingrediente']), None)
        if existente:
            existente['quantidade'] += ing['quantidade']
        else:
            lista.append({
                'ingrediente': ing['ingrediente'],
                'quantidade': ing['quantidade'],
                'unidade': ing['unidade']
            })

    # exibe lista atualizada
    itens = "\n".join(f"• {x['ingrediente']}: {x['quantidade']} {x['unidade']}" for x in lista)
    await update.message.reply_text(f"✅ Receita '{nome}' adicionada!\n\n🛒 Sua lista atual:\n{itens}")

    return await iniciar_lista(update, context)

# --- Seleciona ingrediente e pede quantidade ---
async def lista_selecionar_ingrediente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    escolha = update.message.text
    todos = context.user_data['todos_para_lista']
    match = next((i for i in todos if f"{i['ingrediente']} ({i['unidade']})" == escolha), None)
    if not match:
        await update.message.reply_text("❌ Ingrediente inválido. Tente novamente.")
        return LISTA_INGREDIENTE

    context.user_data['current_lista_ing'] = match
    await update.message.reply_text(f"🔢 Quantos {match['ingrediente']} ({match['unidade']})?")
    return LISTA_QTD

# --- Recebe quantidade e exibe lista atualizada ---
async def lista_qtd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    if not texto.isdigit():
        await update.message.reply_text("❌ Digite apenas números.")
        return LISTA_QTD

    qtd = int(texto)
    ing = context.user_data['current_lista_ing']

    # adiciona ou soma se já existir
    lista = context.user_data['lista_compra']
    existente = next((x for x in lista if x['ingrediente'] == ing['ingrediente']), None)
    if existente:
        existente['quantidade'] += qtd
    else:
        lista.append({
            'ingrediente': ing['ingrediente'],
            'quantidade': qtd,
            'unidade': ing['unidade']
        })

    # mostra lista atualizada
    itens = "\n".join(f"• {x['ingrediente']}: {x['quantidade']} {x['unidade']}" for x in lista)
    await update.message.reply_text(f"✅ Item adicionado!\n\n🛒 Sua lista atual:\n{itens}")

    return await iniciar_lista(update, context)

# --- Seleciona receita e adiciona todos os ingredientes ---
async def lista_receita(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome = update.message.text
    receitas = context.user_data['todas_receitas']
    match = next((r for r in receitas if r['nome'] == nome), None)
    if not match:
        await update.message.reply_text("❌ Receita inválida. Tente novamente.")
        return LISTA_RECEITA

    lista = context.user_data['lista_compra']

    # para cada ingrediente da receita, soma ou adiciona
    for ing in match['ingredientes']:
        existente = next((x for x in lista if x['ingrediente'] == ing['ingrediente']), None)
        if existente:
            existente['quantidade'] += ing['quantidade']
        else:
            lista.append({
                'ingrediente': ing['ingrediente'],
                'quantidade': ing['quantidade'],
                'unidade': ing['unidade']
            })

    # exibe lista atualizada
    itens = "\n".join(f"• {x['ingrediente']}: {x['quantidade']} {x['unidade']}" for x in lista)
    await update.message.reply_text(f"✅ Receita '{nome}' adicionada!\n\n🛒 Sua lista atual:\n{itens}")

    return await iniciar_lista(update, context)


conv_list = ConversationHandler(
    entry_points=[CommandHandler('fazer_lista', iniciar_lista)],
    states={
        LISTA_OPCAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, lista_opcao)],
        LISTA_INGREDIENTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, lista_selecionar_ingrediente)],
        LISTA_QTD: [MessageHandler(filters.TEXT & ~filters.COMMAND, lista_qtd)],
        LISTA_RECEITA: [MessageHandler(filters.TEXT & ~filters.COMMAND, lista_receita)],
    },
    fallbacks=[],
    allow_reentry=True
)