import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import Channel

def start(update: Update, context: CallbackContext) -> None:
    """Start command handler."""
    update.message.reply_text('Bot started. I will automatically delete messages in every chat where I am added, except for videos (MKV, MP4).')

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming messages."""
    message = update.message

    if message.chat.type == 'channel':
        channel_id = message.chat.id
        client = TelegramClient('session_name', API_ID, API_HASH)
        client.start()

        try:
            channel = client(GetFullChannelRequest(channel=channel_id))
            if isinstance(channel.chats[0], Channel):
                client.delete_messages(entity=channel.chats[0], message_ids=[message.message_id])
        except Exception as e:
            print(f'Error deleting message in channel: {str(e)}')
        finally:
            client.disconnect()

def main() -> None:
    """Main function to run the bot."""
    token = os.environ.get('BOT_TOKEN')
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
