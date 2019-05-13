import datetime
import logging
from venv import logger

from telegram import Bot, Update, CallbackQuery
from telegram.ext import CallbackQueryHandler, CommandHandler, RegexHandler, Updater
from telegram.utils.request import Request
from telegram.ext import messagequeue as mq

import Regex
from commands import start, callback_404
from cronometer import cron_callback, CALLBACK_CRON_SAVE, cron_inline, CALLBACK_CRON_UPDATE, \
    CALLBACK_CRON_START, CALLBACK_CRON_STOP, CALLBACK_CRON_DISCARD
from database import startup_mongodb
from help import CALLBACK_HELP_PUBS_DEMO, help_callback, help_inline, CALLBACK_HELP_INTRO, CALLBACK_HELP_HOURS, \
    CALLBACK_HELP_CRON, CALLBACK_HELP_PUBS, CALLBACK_HELP_VIDEOS, CALLBACK_HELP_RETURNS, CALLBACK_HELP_STUDIES, \
    CALLBACK_HELP_REPORT, CALLBACK_HELP_HOURS_DEMO, CALLBACK_HELP_CRON_DEMO, CALLBACK_HELP_VIDEOS_DEMO, \
    CALLBACK_HELP_RETURNS_DEMO, CALLBACK_HELP_STUDIES_DEMO, CALLBACK_HELP_REPORT_DEMO
from hours import CALLBACK_HOURS_ADD_TWO_HOURS, hours_callback, hours_inline, CALLBACK_HOURS_ADD, \
    CALLBACK_HOURS_MINUTES_ADD, CALLBACK_HOURS_ADD_ONE_HOUR, CALLBACK_HOURS_REMOVE_ONE_HOUR, \
    CALLBACK_HOURS_REMOVE_TWO_HOURS, CALLBACK_HOURS_ADD_THIRTY_MINUTES, CALLBACK_HOURS_ADD_TEN_MINUTES, \
    CALLBACK_HOURS_ADD_FIVE_MINUTES, CALLBACK_HOURS_REMOVE_THIRTY_MINUTES, CALLBACK_HOURS_REMOVE_TEN_MINUTES, \
    CALLBACK_HOURS_REMOVE_FIVE_MINUTES, callback_offline_add_hours, callback_offline_add_minutes, \
    callback_offline_remove_minutes, callback_offline_remove_hours
from publications import pubs_inline, pubs_callback, CALLBACK_PUBS_ADD_ONE, CALLBACK_PUBS_ADD_THREE, \
    CALLBACK_PUBS_REMOVE_ONE, pubs_offline_add_callback, pubs_offline_remove_callback
from reports import report_notification_job, reports_callback, reports_inline, CALLBACK_REPORT_LAST_MONTH, \
    CALLBACK_REPORT_CURRENT_MONTH
from returns import returns_inline, returns_callback, CALLBACK_RETURNS_ADD_ONE, CALLBACK_RETURNS_ADD_THREE, \
    CALLBACK_RETURNS_REMOVE_ONE, CALLBACK_RETURNS_LIST, CALLBACK_RETURNS_INSTERESTED, returns_offline_add_callback, \
    returns_offline_remove_callback, returns_people_callback, returns_people_remove_callback
from studies import studies_callback, studies_inline, CALLBACK_STUDIES_ADD_ONE, CALLBACK_STUDIES_ADD_THREE, \
    CALLBACK_STUDIES_REMOVE_ONE, studies_offline_add_callback, studies_offline_remove_callback
from videos import CALLBACK_VIDEO_ADD_ONE, CALLBACK_VIDEO_ADD_THREE, CALLBACK_VIDEO_REMOVE_ONE, video_callback, \
    video_inline, video_offline_add_callback, video_offline_remove_callback


class MQBot(Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_message(*args, **kwargs)


def error(bot: Bot, update: Update, error):
    query: CallbackQuery = update.callback_query

    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def startup():
    print('main called')

    msg_queue = mq.MessageQueue(all_burst_limit=28, all_time_limit_ms=1050)
    request = Request(con_pool_size=8)
    TOKEN = open('campobot/token/token_bot_test.txt', 'r').read().strip()
    campo_bot = MQBot(TOKEN, request=request, mqueue=msg_queue)

    updater = Updater(bot=campo_bot)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    jobs = updater.job_queue
    jobs.run_daily(callback=report_notification_job, time=datetime.time(hour=12, minute=30))

    # Help Handler
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_INTRO))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_HOURS))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_CRON))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_PUBS))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_VIDEOS))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_RETURNS))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_STUDIES))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_REPORT))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_HOURS_DEMO))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_CRON_DEMO))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_VIDEOS_DEMO))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_PUBS_DEMO))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_RETURNS_DEMO))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_STUDIES_DEMO))
    dispatcher.add_handler(CallbackQueryHandler(callback=help_callback, pattern=CALLBACK_HELP_REPORT_DEMO))
    dispatcher.add_handler(RegexHandler(callback=help_inline, pattern=str(Regex.START_WITH_EMOJI_SLASH + Regex.HELP_COMMAND)))

    # Cron Handler
    dispatcher.add_handler(CallbackQueryHandler(callback=cron_callback, pattern=CALLBACK_CRON_START, pass_user_data=True))
    dispatcher.add_handler(CallbackQueryHandler(callback=cron_callback, pattern=CALLBACK_CRON_UPDATE, pass_user_data=True))
    dispatcher.add_handler(CallbackQueryHandler(callback=cron_callback, pattern=CALLBACK_CRON_STOP, pass_user_data=True))
    dispatcher.add_handler(CallbackQueryHandler(callback=cron_callback, pattern=CALLBACK_CRON_SAVE, pass_user_data=True))
    dispatcher.add_handler(CallbackQueryHandler(callback=cron_callback, pattern=CALLBACK_CRON_DISCARD, pass_user_data=True))
    dispatcher.add_handler(RegexHandler(callback=cron_inline, pattern=str(Regex.START_WITH_EMOJI_SLASH + Regex.CRON_COMMAND), pass_user_data=True))

    # Videos Handler
    dispatcher.add_handler(CallbackQueryHandler(callback=video_callback, pattern=CALLBACK_VIDEO_ADD_ONE))
    dispatcher.add_handler(CallbackQueryHandler(callback=video_callback, pattern=CALLBACK_VIDEO_ADD_THREE))
    dispatcher.add_handler(CallbackQueryHandler(callback=video_callback, pattern=CALLBACK_VIDEO_REMOVE_ONE))
    dispatcher.add_handler(RegexHandler(callback=video_offline_add_callback, pattern=Regex.VIDEO_OFFLINE_ADD))
    dispatcher.add_handler(RegexHandler(callback=video_offline_remove_callback, pattern=Regex.VIDEO_OFFLINE_REMOVE))
    dispatcher.add_handler(RegexHandler(callback=video_inline, pattern=str(Regex.START_WITH_EMOJI_SLASH + Regex.VIDEO_COMMAND)))

    # Report Handler
    dispatcher.add_handler(CallbackQueryHandler(callback=reports_callback, pattern=CALLBACK_REPORT_LAST_MONTH))
    dispatcher.add_handler(CallbackQueryHandler(callback=reports_callback, pattern=CALLBACK_REPORT_CURRENT_MONTH))
    dispatcher.add_handler(RegexHandler(callback=reports_inline, pattern=str(Regex.START_WITH_EMOJI_SLASH + Regex.REPORT_COMMAND)))

    # Studies Handler
    dispatcher.add_handler(CallbackQueryHandler(callback=studies_callback, pattern=CALLBACK_STUDIES_ADD_ONE))
    dispatcher.add_handler(CallbackQueryHandler(callback=studies_callback, pattern=CALLBACK_STUDIES_ADD_THREE))
    dispatcher.add_handler(CallbackQueryHandler(callback=studies_callback, pattern=CALLBACK_STUDIES_REMOVE_ONE))
    dispatcher.add_handler(RegexHandler(callback=studies_offline_add_callback, pattern=Regex.STUDIES_OFFLINE_ADD))
    dispatcher.add_handler(RegexHandler(callback=studies_offline_remove_callback, pattern=Regex.STUDIES_OFFLINE_REMOVE))
    dispatcher.add_handler(RegexHandler(callback=studies_inline, pattern=str(Regex.START_WITH_EMOJI_SLASH + Regex.STUDIES_COMMAND)))

    # Pubs Handler
    dispatcher.add_handler(CallbackQueryHandler(callback=pubs_callback, pattern=CALLBACK_PUBS_ADD_ONE))
    dispatcher.add_handler(CallbackQueryHandler(callback=pubs_callback, pattern=CALLBACK_PUBS_ADD_THREE))
    dispatcher.add_handler(CallbackQueryHandler(callback=pubs_callback, pattern=CALLBACK_PUBS_REMOVE_ONE))
    dispatcher.add_handler(RegexHandler(callback=pubs_offline_add_callback, pattern=Regex.PUBS_OFFLINE_ADD))
    dispatcher.add_handler(RegexHandler(callback=pubs_offline_remove_callback, pattern=Regex.PUBS_OFFLINE_REMOVE))
    dispatcher.add_handler(RegexHandler(callback=pubs_inline, pattern=str(Regex.START_WITH_EMOJI_SLASH + Regex.PUBS_COMMAND)))

    # Hours Handler
    dispatcher.add_handler(CallbackQueryHandler(callback=hours_callback, pattern=CALLBACK_HOURS_ADD, pass_user_data=True))
    dispatcher.add_handler(CallbackQueryHandler(callback=hours_callback, pattern=CALLBACK_HOURS_MINUTES_ADD, pass_user_data=True))
    dispatcher.add_handler(CallbackQueryHandler(callback=hours_callback, pattern=CALLBACK_HOURS_ADD_ONE_HOUR, pass_user_data=True))
    dispatcher.add_handler(CallbackQueryHandler(callback=hours_callback, pattern=CALLBACK_HOURS_ADD_TWO_HOURS, pass_user_data=True))
    dispatcher.add_handler(CallbackQueryHandler(callback=hours_callback, pattern=CALLBACK_HOURS_REMOVE_ONE_HOUR, pass_user_data=True))
    dispatcher.add_handler(CallbackQueryHandler(callback=hours_callback, pattern=CALLBACK_HOURS_REMOVE_TWO_HOURS, pass_user_data=True))
    dispatcher.add_handler(CallbackQueryHandler(callback=hours_callback, pattern=CALLBACK_HOURS_ADD_THIRTY_MINUTES))
    dispatcher.add_handler(CallbackQueryHandler(callback=hours_callback, pattern=CALLBACK_HOURS_ADD_TEN_MINUTES))
    dispatcher.add_handler(CallbackQueryHandler(callback=hours_callback, pattern=CALLBACK_HOURS_ADD_FIVE_MINUTES))
    dispatcher.add_handler(CallbackQueryHandler(callback=hours_callback, pattern=CALLBACK_HOURS_REMOVE_THIRTY_MINUTES))
    dispatcher.add_handler(CallbackQueryHandler(callback=hours_callback, pattern=CALLBACK_HOURS_REMOVE_TEN_MINUTES))
    dispatcher.add_handler(CallbackQueryHandler(callback=hours_callback, pattern=CALLBACK_HOURS_REMOVE_FIVE_MINUTES))
    dispatcher.add_handler(RegexHandler(callback=callback_offline_add_hours, pattern=Regex.HOURS_OFFLINE_ADD))
    dispatcher.add_handler(RegexHandler(callback=callback_offline_remove_hours, pattern=Regex.HOURS_OFFLINE_REMOVE))
    dispatcher.add_handler(RegexHandler(callback=callback_offline_add_minutes, pattern=Regex.HOURS_OFFLINE_ADD_MINUTES))
    dispatcher.add_handler(RegexHandler(callback=callback_offline_remove_minutes, pattern=Regex.HOURS_OFFLINE_REMOVE_MINUTES))
    dispatcher.add_handler(RegexHandler(callback=hours_inline, pattern=str(Regex.START_WITH_EMOJI_SLASH + Regex.HOURS_COMMAND)))

    # Returns Handler
    dispatcher.add_handler(CallbackQueryHandler(callback=returns_callback, pattern=CALLBACK_RETURNS_ADD_ONE))
    dispatcher.add_handler(CallbackQueryHandler(callback=returns_callback, pattern=CALLBACK_RETURNS_ADD_THREE))
    dispatcher.add_handler(CallbackQueryHandler(callback=returns_callback, pattern=CALLBACK_RETURNS_REMOVE_ONE))
    dispatcher.add_handler(CallbackQueryHandler(callback=returns_callback, pattern=CALLBACK_RETURNS_LIST))
    dispatcher.add_handler(CallbackQueryHandler(callback=returns_callback, pattern=CALLBACK_RETURNS_INSTERESTED))
    dispatcher.add_handler(RegexHandler(callback=returns_offline_add_callback, pattern=Regex.RETURNS_OFFLINE_ADD))
    dispatcher.add_handler(RegexHandler(callback=returns_offline_remove_callback, pattern=Regex.RETURNS_OFFLINE_REMOVE))
    dispatcher.add_handler(RegexHandler(callback=returns_inline, pattern=str(Regex.START_WITH_EMOJI_SLASH + Regex.RETURNS_COMMAND)))
    dispatcher.add_handler(RegexHandler(callback=returns_people_callback, pattern=Regex.RETURNS_PEOPLE))
    dispatcher.add_handler(RegexHandler(callback=returns_people_remove_callback, pattern=Regex.RETURNS_PEOPLE_REMOVE))

    # Commands Handler
    dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
    dispatcher.add_handler(RegexHandler(callback=callback_404, pattern=Regex.NOT_FOUND_404))  # Must be last one
    dispatcher.add_error_handler(error)

    # Start MongoDB and Bot
    startup_mongodb()
    updater.start_polling()


if __name__ == '__main__':
    startup()
