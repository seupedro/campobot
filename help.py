# Callback Constants
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot, CallbackQuery
from telegram.ext import JobQueue

CALLBACK_HELP_HOURS = 'help_hours'
CALLBACK_HELP_CRON = 'help_cron'
CALLBACK_HELP_PUBS = 'help_pubs'
CALLBACK_HELP_VIDEOS = 'help_videos'
CALLBACK_HELP_RETURNS = 'help_returns'
CALLBACK_HELP_STUDIES = 'help_studies'
CALLBACK_HELP_REPORT = 'help_report'

CALLBACK_HELP_INTRO = 'help_intro'
CALLBACK_HELP_HOURS_DEMO = 'help_hours_demo_video'
CALLBACK_HELP_CRON_DEMO = 'help_cron_demo_video'
CALLBACK_HELP_VIDEOS_DEMO = 'help_videos_demo_video'
CALLBACK_HELP_PUBS_DEMO = 'help_pubs_demo_video'
CALLBACK_HELP_RETURNS_DEMO = 'help_returns_demo_video'
CALLBACK_HELP_STUDIES_DEMO = 'help_studies_demo_video'
CALLBACK_HELP_REPORT_DEMO = 'help_report_demo_video'

CALLBACK_HELP_CONTACT = 'help_contact'

# Keyboards Inline
help_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(u"🕓 Horas", callback_data=CALLBACK_HELP_HOURS),
      InlineKeyboardButton(u"⏱ Cronômetro", callback_data=CALLBACK_HELP_CRON)],

     [InlineKeyboardButton(u"🎞 Vídeos", callback_data=CALLBACK_HELP_VIDEOS),
      InlineKeyboardButton(u"📕 Publicações", callback_data=CALLBACK_HELP_PUBS)],

     [InlineKeyboardButton(u"🏠 Revisitas", callback_data=CALLBACK_HELP_RETURNS),
      InlineKeyboardButton(u"🌱 Estudos", callback_data=CALLBACK_HELP_STUDIES)],

     [InlineKeyboardButton(u"📝 Relatório", callback_data=CALLBACK_HELP_REPORT)]]
)

hours_help_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(u'Início', callback_data=CALLBACK_HELP_INTRO),
      InlineKeyboardButton(u'Demonstração', callback_data=CALLBACK_HELP_HOURS_DEMO)]]
)

cron_help_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(u'Início', callback_data=CALLBACK_HELP_INTRO),
      InlineKeyboardButton(u'Demonstração', callback_data=CALLBACK_HELP_CRON_DEMO)]]
)

videos_help_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(u'Início', callback_data=CALLBACK_HELP_INTRO),
      InlineKeyboardButton(u'Demonstração', callback_data=CALLBACK_HELP_VIDEOS_DEMO)]]
)

pubs_help_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(u'Início', callback_data=CALLBACK_HELP_INTRO),
      InlineKeyboardButton(u'Demonstração', callback_data=CALLBACK_HELP_PUBS_DEMO)]]
)

returns_help_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(u'Início', callback_data=CALLBACK_HELP_INTRO),
      InlineKeyboardButton(u'Demonstração', callback_data=CALLBACK_HELP_RETURNS_DEMO)]]
)

studies_help_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(u'Início', callback_data=CALLBACK_HELP_INTRO),
      InlineKeyboardButton(u'Demonstração', callback_data=CALLBACK_HELP_STUDIES_DEMO)]]
)

report_help_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(u'Início', callback_data=CALLBACK_HELP_INTRO),
      InlineKeyboardButton(u'Demonstração', callback_data=CALLBACK_HELP_REPORT_DEMO)]]
)

home_contact_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(u'Início', callback_data=CALLBACK_HELP_INTRO),
      InlineKeyboardButton(u'Mais Ajuda', url='t.me/pedrohartmann')]]
)

# GIF Constants
HOUR_GIF = 'CgADAQADkwADDkrpRAOJrNQBQlf3Ag'
CRON_VIDEO = 'BAADAQADRgADGHDpRIPcGIvVGQHDAg'
VIDEO_VIDEO = 'BAADAQADmAADDkrpRHl9CyUfjEBhAg'
PUBS_VIDEO = 'BAADAQADRwADGHDpRNRFjZ7xh4ZjAg'
RETURNS_VIDEO = 'BAADAQADmQADDkrpRIPvjeXYKULnAg'
STUDY_VIDEO = 'BAADAQADRQADGHDpRGWAjXX81OM7Ag'
REPORT_VIDEO = 'CgADAQADXgADLpQRRWmfd_4ozPnwAg'


def help_inline(bot: Bot, update: Update):
    update.message.reply_text(text='❓ *Ajuda*\n\n'
                                   "Tem uma dúvida? \n"
                                   "Escolha primeiro uma opção pra que eu possa te ajudar.",
                              reply_markup=help_keyboard,
                              parse_mode='Markdown')


def help_callback(bot: Bot, update: Update):
    query: CallbackQuery = update.callback_query

    if query.data == CALLBACK_HELP_INTRO:
        bot.edit_message_text(text='❓ *Ajuda*\n\n'
                                   "Tem uma dúvida? \n"
                                   "Escolha primeiro uma opção pra que eu possa te ajudar.",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=help_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_HOURS:
        bot.edit_message_text(text='🕓 *Horas*\n\n'
                                   'Esse recurso serve para você *guardar suas horas* de campo durante o mês. \n\n'
                                   'Você adicionar ou remover suas horas usando os botões que tem o sinal de (+) ou (-). \n\n'
                                   'Suas horas são sempre *salvas automaticamente* após pressionar um botão. \n\n'
                                   'Se você ainda estiver com dúvidas, veja um video de demonstração clicando no botão abaixo.',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=hours_help_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_CRON:
        bot.edit_message_text(text='⏱ *Cronômetro*\n\n'
                                   'Esse recurso serve para você *cronômetrar o seu tempo de campo*. \n\n'
                                   'Você pode acompanhar o seu tempo clicando no botão Atualizar. \n\n'
                                   'Seu tempo é *sempre salvo automaticamente após* pressionar o botão Salvar. '
                                   'Se você não iniciou o cronometro na hora certa, você pode Descartar o tempo e adicionar '
                                   'manualmente depois. \n\n'
                                   'Se você ainda estiver com dúvidas, veja um video de demonstração clicando no botão abaixo.',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=cron_help_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_VIDEOS:
        bot.edit_message_text(text='🎞 *Vídeos*\n\n'
                                   'Aqui você pode salvar os vídeos que você mostrou no serviço de campo durante o mês.\n\n'
                                   'Você pode ver o total do mês e adicionar/subtrair os vídeos.\n\n'
                                   'Seus vídeos sempre são *salvos automaticamente* após pressionar um botão. \n\n'
                                   'Se você ainda estiver com dúvidas, veja um video de demonstração clicando no botão abaixo.',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=videos_help_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_PUBS:
        bot.edit_message_text(text='📕 *Publicações*\n\n'
                                   'Salve o número de publicações que você colocou no mês \n\n'
                                   'Você pode acompanhar o total do mês ou adicionar/subtrair as publicações.\n\n'
                                   'Suas publicações sempre *são salvas automaticamente* após pressionar um botão. \n\n'
                                   'Se você ainda estiver com dúvidas, veja um video de demonstração clicando no botão abaixo.',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=pubs_help_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_RETURNS:
        bot.edit_message_text(text='🏠 *Revisitas*\n\n'
                                   'Salve o número de revisitas que você fez durante o mês. \n\n'
                                   'Você pode acompanhar o total do mês ou adicionar/subtrair suas revisitas.\n\n'
                                   'Suas revisitas são sempre *salvas automaticamente* após pressionar um botão. \n\n'
                                   'Se você ainda estiver com dúvidas, veja um video de demonstração clicando no botão abaixo.',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=returns_help_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_STUDIES:
        bot.edit_message_text(text='🌱 *Estudos*\n\n'
                                   'Salve o número de estudos que você fez durante o mês. \n\n'
                                   'Você pode acompanhar o total do mês ou adicionar/subtrair seus estudos.\n\n'
                                   'Seus estudos são sempre *salvos automaticamente* após pressionar um botão. \n\n'
                                   'Se você ainda estiver com dúvidas, veja um video de demonstração clicando no botão abaixo.',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=studies_help_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_REPORT:
        bot.edit_message_text(text='📝 *Relatório*\n\n'
                                   'Esse recurso junta tudo o que você já adicionou durante o mês em um só lugar. \n\n'
                                   'Você pode ver o relatório do *Mês Atual* ou do *Mês passado.* \n\n'
                                   'Pra te ajudar ainda mais, todo ultimo dia do mês você receberá um lembrete de entraga do relatório.\n\n'
                                   'Se você ainda estiver com dúvidas, veja um video de demonstração clicando no botão abaixo.',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=report_help_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_HOURS_DEMO:
        bot.send_animation(animation=HOUR_GIF,
                           chat_id=query.message.chat_id)

        bot.send_message(text='🕓 *Horas*\n\n'
                              'Você ainda tem alguma dúvida? \n'
                              'Tudo bem, eu conheço alguém que pode te ajudar. 😁',
                         chat_id=query.message.chat_id,
                         reply_markup=home_contact_keyboard,
                         parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_CRON_DEMO:
        bot.send_video(video=CRON_VIDEO,
                       chat_id=query.message.chat_id)

        bot.send_message(text='⏱ *Cronômetro*\n\n'
                              'Você ainda tem alguma dúvida? \n'
                              'Tudo bem, eu conheço alguém que pode te ajudar. 😁',
                         chat_id=query.message.chat_id,
                         reply_markup=home_contact_keyboard,
                         parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_VIDEOS_DEMO:
        bot.send_video(video=VIDEO_VIDEO,
                       chat_id=query.message.chat_id)

        bot.send_message(text='🎞 *Vídeos*\n\n'
                              'Você ainda tem alguma dúvida? \n'
                              'Tudo bem, eu conheço alguém que pode te ajudar. 😁',
                         chat_id=query.message.chat_id,
                         reply_markup=home_contact_keyboard,
                         parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_PUBS_DEMO:
        bot.send_video(video=PUBS_VIDEO,
                       chat_id=query.message.chat_id)

        bot.send_message(text='📕 *Publicações*\n\n'
                              'Você ainda tem alguma dúvida? \n'
                              'Tudo bem, eu conheço alguém que pode te ajudar. 😁',
                         chat_id=query.message.chat_id,
                         reply_markup=home_contact_keyboard,
                         parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_RETURNS_DEMO:
        bot.send_video(video=RETURNS_VIDEO,
                       chat_id=query.message.chat_id)

        bot.send_message(text='🏠 *Revisitas*\n\n'
                              'Você ainda tem alguma dúvida? \n'
                              'Tudo bem, eu conheço alguém que pode te ajudar. 😁',
                         chat_id=query.message.chat_id,
                         reply_markup=home_contact_keyboard,
                         parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_STUDIES_DEMO:
        bot.send_video(video=STUDY_VIDEO,
                       chat_id=query.message.chat_id)

        bot.send_message(text='🌱 *Estudos*\n\n'
                              'Você ainda tem alguma dúvida? \n'
                              'Tudo bem, eu conheço alguém que pode te ajudar. 😁',
                         chat_id=query.message.chat_id,
                         reply_markup=home_contact_keyboard,
                         parse_mode='Markdown')

    elif query.data == CALLBACK_HELP_REPORT_DEMO:
        bot.send_animation(animation=REPORT_VIDEO,
                           chat_id=query.message.chat_id)

        bot.send_message(text='📝 *Relatório*\n\n'
                              'Você ainda tem alguma dúvida? \n'
                              'Tudo bem, eu conheço alguém que pode te ajudar. 😁',
                         chat_id=query.message.chat_id,
                         reply_markup=home_contact_keyboard,
                         parse_mode='Markdown')

    query.answer()
