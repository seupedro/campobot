from telegram import Update, Bot, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
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
