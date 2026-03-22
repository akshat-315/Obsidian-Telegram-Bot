import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes
import logging

from config import settings
from services.obsidian import parse_message, create_fleeting_note

logger = logging.getLogger("obsidian_workflow_bot.services.telegram")

_app: Application | None = None

async def handleTelegramMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received message: {update}")
    note_data = parse_message(update.message.text)
    logger.info(f"Parsed message into note data: {note_data}")
    try:
        await asyncio.to_thread(create_fleeting_note, note_data)
        await update.message.reply_text(f"Note '{note_data.title}' saved to Obsidian.")
    except Exception as e:
        logger.error(f"Failed to create fleeting note: {e}")
        await update.message.reply_text("Failed to save note. Please try again.")

async def start_bot():
    telegram_api_key = settings.TELEGRAM_API_KEY

    global _app
    _app = Application.builder().token(telegram_api_key).build()

    _app.add_handler(MessageHandler(filters=None, callback=handleTelegramMessage))
    
    try:
        await _app.initialize()
        await _app.start()
        await _app.updater.start_polling()
    except Exception as e:
        logger.error(f"Error starting Telegram bot: {e}")
        raise e

    logger.info("Telegram bot started successfully")

async def stop_bot():
    global _app
    if _app is None:
        return None
    
    try:
        await _app.updater.stop()
        await _app.stop()
        await _app.shutdown()
        _app = None
        logger.info("Telegram bot stopped successfully")
    except Exception as e:
        logger.error(f"Error stopping Telegram bot: {e}")
        raise e
