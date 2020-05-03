import logging

from question_bot.config import BotConfig
from question_bot.logic import ArtemBot


def cli():
    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    # Setup configuration
    config = BotConfig.from_env()

    # Start bot
    bot = ArtemBot(config, logger)
    bot.run()
