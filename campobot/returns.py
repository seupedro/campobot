# Callback Constants
import re

from pymongo.cursor import Cursor
from telegram import Bot, CallbackQuery, Chat, InlineKeyboardButton, InlineKeyboardMarkup, Update, User, Message, \
    ChatAction

import Regex
import database
from actions import send_action
from commands import reply_main_keyboard
from database import get_returns_db, save_returns_db, save_person_db, get_person_list_db, remove_person_db

CALLBACK_RETURNS_ADD_ONE = 'returns_add_one'
CALLBACK_RETURNS_REMOVE_ONE = 'returns_remove_one'
CALLBACK_RETURNS_ADD_THREE = 'returns_add_three'

CALLBACK_RETURNS_LIST = 'returns_list'
CALLBACK_RETURNS_INSTERESTED = 'returns_interested'

# Keyboards Inline
add_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Adicionar", callback_data=CALLBACK_RETURNS_ADD_ONE)],

     [InlineKeyboardButton("🙋 Interessados", callback_data=CALLBACK_RETURNS_LIST)]]
)

add_remove_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("+3", callback_data=CALLBACK_RETURNS_ADD_THREE),
      InlineKeyboardButton("+1", callback_data=CALLBACK_RETURNS_ADD_ONE),
      InlineKeyboardButton("-1", callback_data=CALLBACK_RETURNS_REMOVE_ONE)],

     [InlineKeyboardButton("🙋 Interessados", callback_data=CALLBACK_RETURNS_LIST)]]
)


@send_action(ChatAction.TYPING)
def returns_inline(bot: Bot, update: Update):
    usr: User = update.effective_user
    return_count = get_returns_db(update)

    if return_count > 0:
        update.message.reply_text(text='🏠 *Revisitas*\n\n'
                                       "Total de Revisitas: " + str(return_count),
                                  reply_markup=add_remove_keyboard, parse_mode='Markdown')

    else:
        update.message.reply_text(text='🏠 *Revisitas*\n\n'
                                       "Você não marcou nenhuma revisita até agora.",
                                  reply_markup=add_keyboard, parse_mode='Markdown')


def returns_callback(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    query: CallbackQuery = update.callback_query
    returns_count = get_returns_db(update)

    if query.data == CALLBACK_RETURNS_ADD_ONE:
        returns_count += 1

        bot.edit_message_text(text='🏠 *Revisitas*\n\n'
                                   'Total de Revisitas: ' + str(returns_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_RETURNS_REMOVE_ONE:
        # Prevent negative values
        if returns_count == 0:
            return query.answer()

        returns_count -= 1

        bot.edit_message_text(text='🏠 *Revisitas*\n\n'
                                   'Total de Revisitas: ' + str(returns_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_RETURNS_ADD_THREE:
        returns_count += 3

        bot.edit_message_text(text='🏠 *Revisitas*\n\n'
                                   'Total de Revisitas: ' + str(returns_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_RETURNS_LIST:
        person_cursor: Cursor = get_person_list_db(update)

        if person_cursor is not None:
            for person in person_cursor:
                bot.send_message(chat_id=chat.id,
                                 text=person.get(database.PERSON_INFO))
        else:
            bot.send_message(chat_id=chat.id,
                             parse_mode='Markdown',
                             text='🙋‍️ *Interessados*\n\n'
                                  'Olá! Você não adicionou ninguém como interessado até agora. '
                                  'Para salvar, basta escrever as todas as informacoes sobre '
                                  'a pessoa interessada usando o teclado abaixo. \n\n'
                                  'Por exemplo, você pode mandar uma mensagem assim e '
                                  'ela será salva automaticamente: ')
            bot.send_message(chat_id=chat.id,
                             text='Lucas de Lima \n'
                                  'Rua Passos Falcone, 501 \n'
                                  'Por que Deus permite o sofrimento?')

    save_returns_db(update, returns_count)
    query.answer()


@send_action(ChatAction.TYPING)
def returns_offline_add_callback(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    returns_count = get_returns_db(update)
    increment = re.findall('\d+', msg.text)

    if increment[0].isdigit():
        returns_count += int(increment[0])
        save_returns_db(update, returns_count)

        bot.send_message(text='✅ Suas revisitas foram adicionados!',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)
    else:
        # Error caught
        bot.send_message(text='😓 Desculpe, algo estranho aconteceu. \n'
                              'Não foi possível atualizar as suas revisitas. '
                              'Tente novamente ou escreva /ajuda',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)

        raise TypeError('Invalid data type in regex', increment[0])


@send_action(ChatAction.TYPING)
def returns_offline_remove_callback(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    returns_count = get_returns_db(update)
    decrement = re.findall('\d+', msg.text)

    if decrement[0].isdigit():
        returns_count -= int(decrement[0])

        # Prevent negative values
        if returns_count < 0:
            returns_count = 0
        save_returns_db(update, returns_count)

        bot.send_message(text='✅ Suas revisitas foram atualizados!',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)
    else:
        # Error caught
        bot.send_message(text='😓 Desculpe, algo estranho aconteceu. \n'
                              'Não foi possível atualizar suas revisitas. '
                              'Tente novamente ou escreva /ajuda',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)

        raise TypeError('Invalid data type in regex', decrement[0])


@send_action(ChatAction.TYPING)
def returns_people_callback(bot: Bot, update: Update):
    msg: Message = update.effective_message
    chat: Chat = update.effective_chat

    save_person_db(update, str(msg.text))
    bot.send_message(chat_id=chat.id,
                     text='✅ Revisita salva!',
                     reply_to_message_id=msg.message_id)


# TODO: Correct spelling
@send_action(ChatAction.TYPING)
def returns_people_remove_callback(bot: Bot, update: Update):
    msg: Message = update.effective_message
    chat: Chat = update.effective_chat

    if msg.reply_to_message is not None:
        deleted_count = remove_person_db(update, msg.reply_to_message.text)
        if deleted_count > 0:
            bot.send_message(chat_id=chat.id,
                             reply_to_message_id=msg.reply_to_message.message_id,
                             text='✅ Apagado')
        else:
            bot.send_message(chat_id=chat.id,
                             reply_to_message_id=msg.reply_to_message.message_id,
                             reply_markup=reply_main_keyboard,
                             text='😕 Hmmm... Parece que voce tentou deletar algo invalido. '
                                  'Tente novamente ou escreva /ajuda \n\n'
                                  'Esse comando serve para apagar 🙋‍ pessoas interessadas. '
                                  'Se voce nao sabe sobre o que eu estou falando, clique no botão 🏡 Revisitas '
                                  'no teclado abaixo. ')
    else:
        bot.send_message(chat_id=chat.id,
                         reply_markup=reply_main_keyboard,
                         text='😓 Desculpe, mas você nao selecionou nada para apagar. \n\n'
                              'Esse comando serve para apagar 🙋‍ pessoas interessadas. '
                              'Voce deve responder uma mensagem com esse comando para apagar. \n\n'
                              'Se voce nao sabe sobre o que eu estou falando, clique no botão 🏡 Revisitas '
                              'no teclado abaixo.')
