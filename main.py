from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.menu import menu_principal
from handlers.receitas import conv_rec
from handlers.ingredientes import conv_ing
from handlers.lista_compras import conv_list
from handlers.excluir import conv_excluir

async def fallback_global(update, context):
    from handlers.menu import menu_principal
    await update.message.reply_text("Comando não reconhecido.")
    await menu_principal(update, context)

def main():
    app = ApplicationBuilder().token("8278075383:AAHk6C5EkezOArg3UGWeA1bffD_Or4sM-sA").build()
    app.add_handler(CommandHandler('start', menu_principal))
    app.add_handler(conv_rec)
    app.add_handler(conv_ing)
    app.add_handler(conv_list)
    app.add_handler(conv_excluir)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_global))

    print("\033[1;92m")
    print("🤖 BOT: online...")
    print("\033[0m")
    app.run_polling()

if __name__ == '__main__':
    main()