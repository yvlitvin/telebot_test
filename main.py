import logging
from emoji import emojize
from telegram import InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, RegexHandler, Filters, \
    MessageHandler
import telegram
import sqlite3
import datetime

now = datetime.datetime.now()
date = str(now.strftime("%d%m%Y"))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR)
logger = logging.getLogger(__name__)

telebot = telegram.Bot('249430682:AAGPbuoGYllOPbPsZyFkuJHY7ooI_aLsAVU')
LOCATION = range(4)


# emoji
logo_atm = emojize(":atm:", use_aliases=True)
logo_bank = emojize(":bank:", use_aliases=True)
logo_ce = emojize(":currency_exchange:", use_aliases=True)
logo_clock = emojize(":clock3:", use_aliases=True)


def start(bot, update):
    chat_id = update.message.chat_id
    location_keyboard = telegram.KeyboardButton(text=logo_bank+"Банкоматы", request_location=True)
    contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
    ce_keyboard = InlineKeyboardButton(logo_ce+"Курсы валют", callback_data=currency)
    custom_keyboard = [[location_keyboard, contact_keyboard], ['/currency']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    bot.sendMessage(chat_id=chat_id,
                    text="Нажмите Банкоматы, чтобы получить список ближайших банокматов\n нажмите, чтобы",
                    reply_markup=reply_markup)
    return LOCATION


def location(bot, update):
    user = update.message.from_user
    chat_id = update.message.chat_id
    user_location = update.message.location
    logger.info("Location of %s: %f / %f"
                % (user.first_name, user_location.latitude, user_location.longitude))

    conn = sqlite3.connect("atm_numbers.sqlite")
    c = conn.cursor()
    c.execute('SELECT * FROM Ukraine ORDER BY ((?-lat)*(?-lat)) + ((? - long)*(? - long)) ASC limit 3',
              (user_location.latitude, user_location.latitude, user_location.longitude, user_location.longitude))
    for row in c:
        lat_atm = row[11]
        lng_atm = row[12]
        site = row[9]
        name = row[1]
        phone = row[10]
        address = row[5]
        city = row[3]
        face = row[6]
        situat = row[7]
        update.message.reply_text(logo_atm + name+ ', ' + city + ', ' + address + ', '+logo_clock + face + ', ' + situat)
        bot.send_location(chat_id, lat_atm, lng_atm)
    c.close()
    conn.close()


def cancel(bot, update):
    return ConversationHandler.END

def currency(bot, update):
    chat_id = update.message.chat_id
    conn = sqlite3.connect("atm_numbers.sqlite")
    c = conn.cursor()
    c.execute('SELECT * FROM currency where date = ' + date)
    for row in c:
        curr = row[1]
        sale_sel = row[2]
        buy = row[3]
        bnbu = row[4]
        bot.sendMessage(chat_id=chat_id, text=logo_ce + ' ' + curr + ' ' + sale_sel + ' ' + buy + ' ' + bnbu)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("249430682:AAGPbuoGYllOPbPsZyFkuJHY7ooI_aLsAVU")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={


            LOCATION: [MessageHandler([Filters.location], location)]



        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('currency', currency))
    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()