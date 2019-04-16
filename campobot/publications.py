from telegram import InlineKeyboardMarkup, InlineKeyboardButton, User, Update, Bot, CallbackQuery

from campobot.database import get_pubs_db, save_pubs_db

CALLBACK_PUBS_ADD_ONE = 'pubs_add_one'
CALLBACK_PUBS_ADD_THREE = 'pubs_add_three'
CALLBACK_PUBS_REMOVE_ONE = 'pubs_remove_one'

# Keyboards Inline
add_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Adicionar", callback_data=CALLBACK_PUBS_ADD_ONE)]]
)

add_remove_keyboard = InlineKeyboardMarkup(

     [[InlineKeyboardButton("+3", callback_data=CALLBACK_PUBS_ADD_THREE),
      InlineKeyboardButton("+1", callback_data=CALLBACK_PUBS_ADD_ONE ),
      InlineKeyboardButton("-1", callback_data=CALLBACK_PUBS_REMOVE_ONE)]]
)


def pubs_inline(bot: Bot, update: Update):
    usr: User = update.effective_user
    pubs_count = get_pubs_db(update)

    if pubs_count > 0:
        update.message.reply_text(text=u'📕 *Publicações*\n\n'
                                       u'Total de Publicações: ' + str(pubs_count),
                                  reply_markup=add_remove_keyboard, parse_mode='Markdown')

    else:
        update.message.reply_text(text=u'📕 *Publicações*\n\n' 
                                       u'Você não colocou nenhuma publicação até agora.',
                                  reply_markup=add_keyboard, parse_mode='Markdown')


def pubs_callback(bot: Bot, update: Update):
    query: CallbackQuery = update.callback_query
    pubs_count = get_pubs_db(update)

    if query.data == CALLBACK_PUBS_ADD_ONE:
        pubs_count += 1

        bot.edit_message_text(text='📕 *Publicações*\n\n'
                                   u'Total de Publicações: ' + str(pubs_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_PUBS_REMOVE_ONE:
        # Prevent negative values
        if pubs_count == 0:
            return query.answer()

        pubs_count -= 1

        bot.edit_message_text(text='📕 *Publicações*\n\n'
                                   u'Total de Publicações: ' + str(pubs_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_PUBS_ADD_THREE:
        pubs_count += 3

        bot.edit_message_text(text='📕 *Publicações*\n\n'
                                   u'Total de Publicações: ' + str(pubs_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    save_pubs_db(update, pubs_count)
    query.answer()
