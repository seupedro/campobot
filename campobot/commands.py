from campobot.database import save_profile_db
from telegram import Bot, Chat, KeyboardButton, Message, ReplyKeyboardMarkup, Update, User

reply_main_keyboard = ReplyKeyboardMarkup([[KeyboardButton(u"🕓 Horas"),
                                            KeyboardButton(u"⏱ Cronômetro")],

                                           [KeyboardButton(u"🎞 Vídeos"),
                                            KeyboardButton(u"📕 Publicações")],

                                           [KeyboardButton(u"🏠 Revisitas"),
                                            KeyboardButton(u"🌱 Estudos"),
                                            KeyboardButton(u'📝 Relatório')]], resize_keyboard=True)


def start(bot, update, user_data=None):
    usr: User = update.effective_user
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    save_profile_db(bot, update)

    bot.send_message(chat_id=chat.id,
                     text="Olá " + chat.first_name + ", como vai?\n\n"
                          "Use o teclado abaixo para salvar no seu relatório. "
                          "Em caso do dúvidas, escreva /ajuda",
                     reply_markup=reply_main_keyboard)


def callback_404(bot: Bot, update: Update):
    usr: User = update.effective_user
    chat: Chat = update.effective_chat

    bot.send_message(text='😥 Desculpe {} \n'
                          'Não consegui te entender. \n\n'
                          'Use o teclado abaixo ou escreva /ajuda para ter mais informações'
                     .format(usr.first_name),
                     chat_id=chat.id,
                     parse_mode='Markdown',
                     reply_markup=reply_main_keyboard)







