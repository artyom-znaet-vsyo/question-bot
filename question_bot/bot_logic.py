"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from question_bot.config import BotConfig


class ArtemBot:
    def __init__(self, config: BotConfig, logger: logging.Logger):
        self.logger = logger
        self.updater = Updater(config.TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.bind()

    def bind(self):
        # on different commands - answer in Telegram
        self.dispatcher.add_handler(CommandHandler("start", self.handle_start))
        self.dispatcher.add_handler(CommandHandler("help", self.handle_help))

        # on noncommand i.e message - echo the message on Telegram
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.handle_echo))

        # log all errors
        self.dispatcher.add_error_handler(self.handle_error)

    def handle_start(self, update, context):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def handle_help(self, update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    def handle_echo(self, update, context):
        """Echo the user message."""
        update.message.reply_text(update.message.text)

    def handle_error(self, update, context):
        """Log Errors caused by Updates."""
        self.logger.warning(f'Update "{update}" caused error "{context.error}"')

    def run(self):
        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()


if __name__ == "__main__":
    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    config = BotConfig.from_env()
    bot = ArtemBot(config, logger)
    bot.run()
