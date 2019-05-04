import time

from actions import send_action
from database import save_cron_db
from telegram import InlineKeyboardButton, Update, Bot, InlineKeyboardMarkup, CallbackQuery, ChatAction

# Constants
START_CTIMER = 'start_ctime'
TOTAL_CTIMER = 'stop_ctime'

# Callback Constants
CALLBACK_CRON_START = 'cron_start'
CALLBACK_CRON_UPDATE = 'cron_update'
CALLBACK_CRON_STOP = 'cron_stop'
CALLBACK_CRON_SAVE = 'cron_save'
CALLBACK_CRON_DISCARD = 'cron_discard'

# Keyboards Inline
start_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Iniciar", callback_data=CALLBACK_CRON_START)]]
)

refresh_stop_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Atualizar", callback_data=CALLBACK_CRON_UPDATE),
      InlineKeyboardButton("Parar", callback_data=CALLBACK_CRON_STOP)]]
)

save_discard_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Salvar", callback_data=CALLBACK_CRON_SAVE),
      InlineKeyboardButton("Descartar", callback_data=CALLBACK_CRON_DISCARD)]]
)


@send_action(ChatAction.TYPING)
def cron_inline(bot: Bot, update: Update, user_data: dict):

    if START_CTIMER in user_data:
        current_cron = time.time() - user_data[START_CTIMER]

        update.message.reply_text('⏱ *Cronômetro*\n\n'
                                  "Seu tempo até agora:\n"
                                  "{}".format(seconds_to_hours(current_cron)),
                                  reply_markup=refresh_stop_keyboard, parse_mode='Markdown')

    else:
        update.message.reply_text('⏱ *Cronômetro*\n'
                                  "Toque no botão abaixo para começar.",
                                  reply_markup=start_keyboard, parse_mode='Markdown')


def cron_callback(bot: Bot, update: Update, user_data: dict):
    query: CallbackQuery = update.callback_query

    if query.data == CALLBACK_CRON_START:
        user_data[START_CTIMER] = time.time()

        bot.edit_message_text(text='⏱ *Cronômetro*\n\n'
                                   'Estamos cronometrando. \n'
                                   'Bom campo! 🌱',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=refresh_stop_keyboard,
                              parse_mode='markdown')

    elif query.data == CALLBACK_CRON_UPDATE:
        if user_data.get(START_CTIMER) is None:
            return query.answer(text='⚠  Use o mesmo cronômetro ', show_alert=False)

        current_cron = time.time() - user_data[START_CTIMER]

        bot.edit_message_text(text='⏱ *Cronômetro*\n\n'
                                   "Seu tempo até agora:\n"
                                   "{}".format(seconds_to_hours(current_cron)),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=refresh_stop_keyboard,
                              parse_mode='markdown')

    elif query.data == CALLBACK_CRON_STOP:
        if user_data.get(START_CTIMER) is None:
            return query.answer(text='⚠  Use o mesmo cronômetro ', show_alert=False)

        user_data[TOTAL_CTIMER] = time.time() - user_data[START_CTIMER]
        user_data.pop(START_CTIMER)

        bot.edit_message_text(text='⏱ *Cronômetro*\n\n'
                                   'Tempo total: \n' + seconds_to_hours(user_data[TOTAL_CTIMER]),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=save_discard_keyboard,
                              parse_mode='markdown')

    elif query.data == CALLBACK_CRON_SAVE:
        save_cron_db(bot, update, user_data[TOTAL_CTIMER])

        bot.edit_message_text(text='⏱ *Cronômetro*\n\n'
                                   '{} foram adicionados no seu relatório. Quer iniciar novamente?'
                              .format(seconds_to_hours(user_data[TOTAL_CTIMER])),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=start_keyboard,
                              parse_mode='markdown')

    elif query.data == CALLBACK_CRON_DISCARD:
        if START_CTIMER in user_data:
            user_data.pop(START_CTIMER)

        bot.edit_message_text(text='⏱ *Cronômetro*\n\n'
                                   'Cronômetro zerado. Quer iniciar novamente?',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=start_keyboard,
                              parse_mode='markdown')

    query.answer()


def seconds_to_hours(seconds: float):
    if seconds <= 60:
        return time.strftime('Só %S segundos...', time.gmtime(seconds))
    if seconds <= 120:
        return time.strftime('%M minuto', time.gmtime(seconds))
    if seconds <= 3600:
        return time.strftime('%M minutos', time.gmtime(seconds))
    if seconds <= 7200:
        return time.strftime('%H hora e %M minutos', time.gmtime(seconds))
    if seconds > 7200:
        return time.strftime('%H horas e %M minutos', time.gmtime(seconds))
