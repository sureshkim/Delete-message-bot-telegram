import os
from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    """Start command handler."""
    update.message.reply_text('Bot started. Please enter the channel ID from which you want to delete upcoming messages.')

def handle_channel_id(update: Update, context: CallbackContext) -> None:
    """Handle the user-provided channel ID."""
    if 'waiting_for_channel_id' in context.bot_data and context.bot_data['waiting_for_channel_id']:
        channel_id = update.message.text.strip()  # Get the channel ID entered by the user

        # Get the list of messages in the channel
        messages = context.bot.get_chat(channel_id).get_messages(limit=100)

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

        # Reset the waiting_for_channel_id flag
        context.bot_data['waiting_for_channel_id'] = False
    else:
        update.message.reply_text('Please start the bot first to enter the channel ID.')

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

    # Set the waiting_for_channel_id flag to True
    dispatcher.bot_data['waiting_for_channel_id'] = True

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
