import logging
import yaml
import os, random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# load credentials

credentials = yaml.load(open("credentials.yml"), Loader=yaml.SafeLoader)
token = credentials["token"]

img_dir = "deepfriedmemes"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Bot initialized.\nType /fryme to continue.")


def fryme(update, context):
    # sends a random deep fried meme
    img = random.choice(os.listdir(img_dir))  # change dir name to whatever
    context.bot.send_photo(
        chat_id=update.effective_chat.id, photo=open(img_dir + "/" + img, "rb")
    )


def echo(update, context):
    update.message.reply_text("Type /fryme you illiterate fuck.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("fryme", fryme))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
