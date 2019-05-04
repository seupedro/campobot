import re

from telegram import Update, Bot, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup, Chat, Message, ChatAction

from actions import send_action
from commands import reply_main_keyboard
from database import get_videos_db, save_videos_db


# Callback Constants
CALLBACK_VIDEO_ADD_ONE = 'video_add_one'
CALLBACK_VIDEO_REMOVE_ONE = 'video_remove_one'
CALLBACK_VIDEO_ADD_THREE = 'video_add_three'

# Keyboards Inline
add_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Adicionar", callback_data=CALLBACK_VIDEO_ADD_ONE)]]
)

add_remove_keyboard = InlineKeyboardMarkup(
     [[InlineKeyboardButton("+3", callback_data=CALLBACK_VIDEO_ADD_THREE),
      InlineKeyboardButton("+1", callback_data=CALLBACK_VIDEO_ADD_ONE),
      InlineKeyboardButton("-1", callback_data=CALLBACK_VIDEO_REMOVE_ONE)]]
)

@send_action(ChatAction.TYPING)
def video_inline(bot: Bot, update: Update):
    video_count = get_videos_db(update)

    if video_count > 0:
        update.message.reply_text(text='🎞 *Vídeos*\n\n'
                                       "Total de Vídeos: " + str(video_count),
                                  reply_markup=add_remove_keyboard, parse_mode='Markdown')

    else:
        update.message.reply_text(text='🎞 *Vídeos*\n\n' 
                                       "Você não marcou nenhum vídeo até agora.",
                                  reply_markup=add_keyboard, parse_mode='Markdown')


def video_callback(bot: Bot, update: Update):
    query: CallbackQuery = update.callback_query
    video_count = get_videos_db(update)

    if query.data == CALLBACK_VIDEO_ADD_ONE:
        video_count += 1

        bot.edit_message_text(text='🎞 *Vídeos*\n\n'
                                   'Total de Vídeos: ' + str(video_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_VIDEO_REMOVE_ONE:
        # Prevent negative values
        if video_count == 0:
            return query.answer()

        video_count -= 1

        bot.edit_message_text(text='🎞 *Vídeos*\n\n'
                                   'Total de Vídeos: ' + str(video_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_VIDEO_ADD_THREE:
        video_count += 3

        bot.edit_message_text(text='🎞 *Vídeos*\n\n'
                                   'Total de Vídeos: ' + str(video_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    save_videos_db(update, video_count)
    query.answer()


@send_action(ChatAction.TYPING)
def video_offline_add_callback(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    videos_count = get_videos_db(update)
    increment = re.findall('\d+', msg.text)

    if increment[0].isdigit():
        videos_count += int(increment[0])
        save_videos_db(update, videos_count)

        bot.send_message(text='✅ Seus vídeos foram adicionados!',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)
    else:
        # Error caught
        bot.send_message(text='😓 Desculpe, algo estranho aconteceu. \n'
                              'Não foi possível adicionar seus minutos. '
                              'Tente novamente ou escreva /ajuda',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)

        raise TypeError('Invalid data type in regex', increment[0])


@send_action(ChatAction.TYPING)
def video_offline_remove_callback(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    videos_count = get_videos_db(update)
    decrement = re.findall('\d+', msg.text)

    if decrement[0].isdigit():
        videos_count -= int(decrement[0])

        # Prevent negative values
        if videos_count < 0:
            videos_count = 0
        save_videos_db(update, videos_count)

        bot.send_message(text='✅ Seus vídeos foram atualizados!',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)
    else:
        # Error caught
        bot.send_message(text='😓 Desculpe, algo estranho aconteceu. \n'
                              'Não foi possível adicionar seus minutos. '
                              'Tente novamente ou escreva /ajuda',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)

        raise TypeError('Invalid data type in regex', decrement[0])

