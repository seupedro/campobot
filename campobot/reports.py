import datetime

from telegram import Bot, Message, Update, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import Job

from campobot import hours, database
from campobot.database import get_report_db, get_profile_list_db

# Callbacks
CALLBACK_REPORT_LAST_MONTH = "report_last_month"
CALLBACK_REPORT_CURRENT_MONTH = "report_current_month"

# Inline Keyboard
CONTACT_KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Contato", url='t.me/pedrohartmann' )]]
)

LAST_MONTH_KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Mês Passado", callback_data=CALLBACK_REPORT_LAST_MONTH)]]
)


CURRENT_MONTH_KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Mês Atual", callback_data=CALLBACK_REPORT_CURRENT_MONTH)]]
)


def reports_inline(bot: Bot, update: Update):
    msg: Message = update.effective_message
    report_count = get_report_db(update)

    if report_count is None:
        msg.reply_text(text=u'📝 *Relatório*\n\n' +
                            u'Olá, como vai? \n'
                            u'Por enquanto seu relatório está vazio. '
                            u'Tente adicionar algo primeiro.',
                       reply_markup=LAST_MONTH_KEYBOARD,
                       parse_mode='Markdown')
    else:
        month_report = report_generator(report_count)
        msg.reply_text(text=month_report,
                       reply_markup=LAST_MONTH_KEYBOARD,
                       parse_mode='Markdown')


def reports_callback(bot, update):
    query: CallbackQuery = update.callback_query

    if query.data == CALLBACK_REPORT_LAST_MONTH:
        last_month_number = datetime.datetime.now().month - 1
        last_report_cursor = get_report_db(update, month=last_month_number)

        if last_report_cursor is not None:
            month_report = report_generator(last_report_cursor)
            bot.edit_message_text(text=month_report,
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  reply_markup=CURRENT_MONTH_KEYBOARD,
                                  parse_mode='Markdown')

        else:
            return query.answer(text='⚠  Você não relatou no mês passado')

    elif query.data == CALLBACK_REPORT_CURRENT_MONTH:
        report_cursor = get_report_db(update)

        if report_cursor is not None:
            month_report = report_generator(report_cursor)
            bot.edit_message_text(text=month_report,
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  reply_markup=LAST_MONTH_KEYBOARD,
                                  parse_mode='Markdown')
        else:
            return query.answer(text='⚠  Você não relatou nada nesse mês')

    query.answer()


def report_generator(report_count: dict):
    month = report_count.get('month')
    hours_total = report_count.get(u'hours')
    videos_total = report_count.get(u'videos')
    pubs_total = report_count.get(u'publications')
    returns_total = report_count.get(u'returns')
    studies_total = report_count.get(u'studies')

    month_report = u'📝 *Relatório de {}*'.format(ptbr_month_name(month)) + '\n\n'
    if hours_total is not None:
        month_report += u'🕓 Horas: ' + hours.seconds_to_hours(hours_total) + '\n\n'
    else:
        month_report += u'🕓 Horas: 0:00' + '\n\n'

    if videos_total is not None:
        month_report += u'🎞 Vídeos: ' + str(videos_total) + '\n\n'
    else:
        month_report += u'🎞 Vídeos: 0' + '\n\n'

    if pubs_total is not None:
        month_report += u'📕 Publicações: ' + str(pubs_total) + '\n\n'
    else:
        month_report += u'📕 Publicações: 0' + '\n\n'

    if returns_total is not None:
        month_report += u'🏠 Revisitas: ' + str(returns_total) + '\n\n'
    else:
        month_report += u'🏠 Revisitas: 0' + '\n\n'

    if studies_total is not None:
        month_report += u'🌱 Estudos: ' + str(studies_total) + '\n\n'
    else:
        month_report += u'🌱 Estudos: 0' + '\n\n'

    return month_report


def ptbr_month_name(month):
    month_list = {
        1: u'Janeiro',
        2: u'Fevereiro',
        3: u'Março',
        4: u'Abril',
        5: u'Maio',
        6: u'Junho',
        7: u'Julho',
        8: u'Agosto',
        9: u'Setembro',
        10: u'Outubro',
        11: u'Novembro',
        12: u'Dezembro',
    }

    return month_list.get(month)


def report_notification_job(bot: Bot, job: Job):
    today = datetime.datetime.now().day
    month = datetime.datetime.now().month
    profile_list = get_profile_list_db()

    if (today == 28 and month == 2 or today == 30) \
            and profile_list is not None:

        for profile in profile_list:
            chat_id = profile.get(database.CHAT_ID)
            report_user = get_report_db(chat_id=chat_id)

            if report_user is not None:
                month_report = report_generator(report_user)

                bot.send_message(text=month_report +
                                 'Este é um lembrete do seu relatório. \n'
                                 'Parabéns por ter se esforçando no campo. Continue assim!',
                                 chat_id=chat_id,
                                 parse_mode='Markdown')

            else:
                bot.send_message(text='Olá {}, tudo bem? \n\n'
                                      'Eu notei que esse mês você não chegou a usar este assistente. 😢 \n'
                                      'Tem alguma coisa que eu poderia melhorar? \n\n'
                                      'O Campo Fácil foi fruto de um longo trabalho árduo, feito com muito carinho para ajudar os publicadores e pioneiros a marcarem suas horas no serviço de campo. \n\n'
                                      'Ele foi feito para funcionar de uma forma simples, para que até mesmo pessoas com pouca intimidade com celulares, como os idosos, possam tirar aproveito. \n\n'
                                      'Caso você não sabia como usar, você pode tirar suas dúvidas escrevendo /ajuda e uma lista com explicação de cada função aparecer. \n\n'
                                      'Mas se mesmo assim você achou que falta alguma coisa ou que o Campo Fácil tem algo a melhorar, eu gostaria muito de saber. Você pode me enviar uma mensagem no contato abaixo. \n\n'
                                      'Espero te ver no mês que vem. \n'
                                      'Fique com Jeová! 🌿 \n\n'.format(profile.get(database.USER_FIRSTNAME)),
                                 chat_id=chat_id,
                                 reply_markup=CONTACT_KEYBOARD,
                                 parse_mode='Markdown')


