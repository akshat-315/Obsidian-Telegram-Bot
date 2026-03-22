from telegram.ext import Application 
import logging

async def start_bot():
    _app = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

    
    await _app.initialize()
    await _app.start()
    await _app.updater.start_polling()

