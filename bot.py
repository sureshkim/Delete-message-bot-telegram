import os
from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    """Start command handler."""
    update.message.reply_text('Bot started. I will automatically delete messages in every chat where I am added, except for videos (MKV, MP4).')

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming messages."""
    message = update.message

    if message.video or (message.document and message.document.file_name.endswith(('.mkv', '.MP4'))):
        # Skip videos, MKV files, and MP4 files
        return

    # Delete the message
    context.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)

def main() -> None:
    """Main function to run the bot."""
    # Get the Telegram bot token from the environment variable
    token = os.environ.get('TOKEN')

    if token is None:
        raise ValueError('Telegram bot token not found. Make sure to set the TOKEN environment variable.')

    updater = Updater(token)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.all, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
          
