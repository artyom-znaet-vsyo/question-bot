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

from telegram.update import Update as TelegramUpdate
from telegram.ext.callbackcontext import CallbackContext as TelegramCallbackContext
from telegram.ext import CommandHandler, Updater

from question_bot.config import BotConfig
from question_bot.integrations import save_question_to_airtable
from question_bot.models import Question


class ArtemBot:
    def __init__(self, config: BotConfig, logger: logging.Logger):
        self.logger = logger
        self.updater = Updater(config.TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.bind()

        self.logger.info('Goliath online')

    def bind(self):
        # on different commands - answer in Telegram
        self.dispatcher.add_handler(CommandHandler("start", self.handle_start))
        self.dispatcher.add_handler(CommandHandler("help", self.handle_help))
        self.dispatcher.add_handler(CommandHandler("vopros", self.handle_vopros))

        # log all errors
        self.dispatcher.add_error_handler(self.handle_error)

    def handle_start(self, update: TelegramUpdate, context: TelegramCallbackContext):
        """Send a message when the command /start is issued."""
        update.message.reply_text(
            '. '.join(
                [
                    'Привет',
                    ' Я тут чтобы помочь вам отправлять сообщения Артёму',
                    'Вы можете не знать Артёма, но Артём знает всё за вас!',
                ]
            )
        )

    def handle_help(self, update: TelegramUpdate, context: TelegramCallbackContext):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Отвечай на сообщения с вопросом и меть их как /vopros')

    def handle_vopros(self, update: TelegramUpdate, context: TelegramCallbackContext):
        """Handle user vopros"""
        message = update.message
        if message['chat']['type'] != 'group':
            update.message.reply_text('Я записываю только вопросы в группах, сорян')
            self.logger.debug(f'Нам пишут в личку, {update.message}')
            return

        question = Question.from_updater_message(message)
        if question is None:
            update.message.reply_text(
                'Не понял вопроса. Используй команду /vopros как реплай к сообщению с вопросом'
            )
            return

        response = save_question_to_airtable(question)
        new_question_id = response['records'][0]['fields']['QuestionNumber']
        self.logger.debug(response)
        update.message.reply_text(f'Вопрос записан. Номер вопроса: {new_question_id}')

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
