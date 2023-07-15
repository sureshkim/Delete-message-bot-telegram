import os
from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    """Start command handler."""
    update.message.reply_text('Bot started. Please enter the channel ID from which you want to delete upcoming messages.')

def handle_channel_id(update: Update, context: CallbackContext) -> None:
    """Handle the user-provided channel ID."""
    channel_id = update.message.text.strip()  # Get the channel ID entered by the user
    
    # Get the list of upcoming messages in the channel
    messages = context.bot.get_chat_messages(chat_id=channel_id, limit=100)

    for message in messages:
        if not isinstance(message, Message):
            # Skip non-message items
            continue
        
        if message.document or message.video:
            # Skip messages that are videos or documents
            continue
        
        # Delete the message
        context.bot.delete_message(chat_id=channel_id, message_id=message.message_id)

    update.message.reply_text('All upcoming messages (excluding videos and documents) have been deleted.')

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
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_channel_id))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
