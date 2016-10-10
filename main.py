import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, RegexHandler, Filters, MessageHandler
import telegram
import sqlite3
import json
import urlfetch
from inputModel import inputModel


conn = sqlite3.connect("atm_numbers.sqlite")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
GENDER, PHOTO, LOCATION, BIO = range(4)

def post(self):
    urlfetch.set_default_fetch_deadline(60)
    body = json.loads(self.request.body)

    # Console Log input message from user
    logging.info('request body:')
    logging.info(json.dumps(body))  # escape " u' " from input

    """
        Fetch user input
    """
    self.response.write(json.dumps(body))  # QUESTION: What does response() do exactly?
    newInput = inputModel(body)  # Initialize input model with user input

    update_id = newInput.getUpdateID()
    message_id = newInput.getMessageID()
    text = newInput.getText()
    fromID = newInput.getFromID()
    fromUserName = newInput.getFromName()
    chat_id = newInput.getChatID()
    location = newInput.getLocation()
    lat = newInput.getLat()
    lng = newInput.getLng()

telebot = telegram.Bot('249430682:AAGPbuoGYllOPbPsZyFkuJHY7ooI_aLsAVU')


def start(bot, update):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query

    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


    return LOCATION

def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
    contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
    custom_keyboard = [[location_keyboard, contact_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
    chat_id = telebot.get_updates()[0].message.chat_id
    bot.sendMessage(chat_id=chat_id,
                 text="Would mind to share location and contact with me ?",
                 reply_markup=reply_markup)
    telebot.send_location(chat_id, user_location.latitude, user_location.longitude)
    c = conn.cursor()
    c.execute('SELECT lat, long FROM Ukraine ORDER BY ((?-lat)*(?-lat)) + ((? - long)*(? - long)) ASC limit 3',(user_location.latitude,user_location.latitude,user_location.longitude,user_location.longitude))
    reply_markup = telegram.ReplyKeyboardHide()
    bot.sendMessage(chat_id=chat_id, text="I'm back.", reply_markup=reply_markup)






# Create the Updater and pass it your bot's token.
updater = Updater("249430682:AAGPbuoGYllOPbPsZyFkuJHY7ooI_aLsAVU")

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('location', location))

updater.dispatcher.add_error_handler(error)




# Start the Bot
updater.start_polling()

# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT
updater.idle()