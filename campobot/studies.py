# Callback Constants
import re

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Update, Bot, Message, Chat

from commands import reply_main_keyboard
from database import get_studies_db, save_studies_db

CALLBACK_STUDIES_ADD_ONE = 'studies_add_one'
CALLBACK_STUDIES_REMOVE_ONE = 'studies_remove_one'
CALLBACK_STUDIES_ADD_THREE = 'studies_add_three'

# Keyboards Inline
add_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Adicionar", callback_data=CALLBACK_STUDIES_ADD_ONE)]]
)

add_remove_keyboard = InlineKeyboardMarkup(
     [[InlineKeyboardButton("+3", callback_data=CALLBACK_STUDIES_ADD_THREE),
      InlineKeyboardButton("+1", callback_data=CALLBACK_STUDIES_ADD_ONE ),
      InlineKeyboardButton("-1", callback_data=CALLBACK_STUDIES_REMOVE_ONE)]]
)


def studies_inline(bot: Bot, update: Update):
    studies_count = get_studies_db(update)

    if studies_count > 0:
        update.message.reply_text(text='🌱 *Estudos*\n\n'
                                       "Total de Estudos: " + str(studies_count),
                                  reply_markup=add_remove_keyboard, parse_mode='Markdown')

    else:
        update.message.reply_text(text='🌱 *Estudos*\n\n' 
                                       "Você não marcou nenhum estudo até agora.",
                                  reply_markup=add_keyboard, parse_mode='Markdown')


def studies_callback(bot: Bot, update: Update):
    query: CallbackQuery = update.callback_query
    studies_count = get_studies_db(update)

    if query.data == CALLBACK_STUDIES_ADD_ONE:
        studies_count += 1

        bot.edit_message_text(text='🌱 *Estudos*\n\n'
                                   'Total de Estudos: ' + str(studies_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_STUDIES_REMOVE_ONE:
        # Prevent negative values
        if studies_count == 0:
            return query.answer()

        studies_count -= 1

        bot.edit_message_text(text='🌱 *Estudos*\n\n'
                                   'Total de Estudos: ' + str(studies_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_STUDIES_ADD_THREE:
        studies_count += 3

        bot.edit_message_text(text='🌱 *Estudos*\n\n'
                                   'Total de Estudos: ' + str(studies_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    save_studies_db(update, studies_count)
    query.answer()


def studies_offline_add_callback(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    studies_count = get_studies_db(update)
    increment = re.findall('\d+', msg.text)

    if increment[0].isdigit():
        studies_count += int(increment[0])

        # Prevent negative values
        if studies_count < 0:
            studies_count = 0
        save_studies_db(update, studies_count)

        bot.send_message(text='✅ Seus estudos foram adicionados!',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)
    else:
        # Error caught
        bot.send_message(text='😓 Desculpe, algo estranho aconteceu. \n'
                              'Não foi possível adicionar seus estudos. '
                              'Tente novamente ou escreva /ajuda',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)

        raise TypeError('Invalid data type in regex', increment[0])


def studies_offline_remove_callback(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    studies_count = get_studies_db(update)
    decrement = re.findall('\d+', msg.text)

    if decrement[0].isdigit():
        studies_count -= int(decrement[0])

        # Prevent negative values
        if studies_count < 0:
            studies_count = 0
        save_studies_db(update, studies_count)

        bot.send_message(text='✅ Seus estudos foram atualizados!',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)
    else:
        # Error caught
        bot.send_message(text='😓 Desculpe, algo estranho aconteceu. \n'
                              'Não foi possível adicionar seus estudos. '
                              'Tente novamente ou escreva /ajuda',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)

        raise TypeError('Invalid data type in regex', decrement[0])

