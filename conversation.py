import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, User, Location
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, RegexHandler, Filters, \
    MessageHandler
import telegram
import sqlite3
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

LOCATION = range(4)

def start(bot, update):
    location_keyboard = telegram.KeyboardButton(text="location", request_location=True)
    contact_keyboard = telegram.KeyboardButton(text="contact", request_contact=True)
    open_location = telegram.KeyboardButton(text="/location")
    custom_keyboard = [[location_keyboard, contact_keyboard, open_location],
                       [location_keyboard, contact_keyboard, open_location]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
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
        update.message.reply_text(name+', '+city+', '+address+', '+face+', '+situat)
        bot.send_location(chat_id, lat_atm, lng_atm)

def cancel(bot, update):
    return ConversationHandler.END


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


            LOCATION: [MessageHandler([Filters.location], location),]



        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()