# import telebot
from telebot import types
import asyncio

from telebot.async_telebot import AsyncTeleBot

# from Warning import *


#### Julian neu #####

with open("token.txt") as file:
    token = file.read()
bot = AsyncTeleBot(token)

@bot.message_handler(commands=['start'])
async def handle_start(message):
    #print(message)
    button_akt_Meldung = types.InlineKeyboardButton('Aktuelle Meldungen zum Wetter', callback_data='akt_Meldung')
    button_allg = types.InlineKeyboardButton('Allgemeine Informationen zum Katastrophenschutz', callback_data='allg')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_allg)

    await bot.reply_to(message, text='Keyboard example', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
async def handle_button_click(call):
    match call.data:
        case "allg":
            # Hier wird die Funktion aufgerufen, die du mit Button 1 verknüpfen möchtest
            await function_allg(call.message)
        case "akt_Meldung":
            # Hier wird die Funktion aufgerufen, die du mit Button 1 verknüpfen möchtest
            await function_akt_meldungen(call.message)

        case _:
            # Hier wird die Funktion aufgerufen, die du mit Button 2 verknüpfen möchtest
            await bot.send_message(call.message.chat.id, "Der Button ist nicht angebunden.")


async def function_allg(message):
    # hier bitte den Zaubereipart einsenden
    antwort = "Du möchtest allgemeine Informationen"
    await bot.send_message(message, antwort)

async def function_akt_meldungen(message):
    # hier bitte Pauls abfrage einfügen
    antwort = "Du möchtest Wetter Informationen"
    await bot.send_message(message, antwort)

# Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
# async def send_welcome(message):
#     await bot.reply_to(message, """hhjvkhv\
#             Hi there, I am EchoBot.
#             I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
#             """)

@bot.message_handler(func=lambda message: True)
async def get_Message(message):
    frage = message.text
    
    await bot.reply_to(message, frage)




asyncio.run(bot.polling())






# ### Paul alt ####
# with open("token.txt") as file:
#     token = file.read()

# bot = telebot.TeleBot(token)
# frage = ""

# # Startnachricht 
# startnachricht = "Disclaimer zu unserem Chatbot: ..."
# markup = types.InlineKeyboardMarkup()
# button = types.InlineKeyboardButton('Aktuelle Informationen zu Warnungen', callback_data='api_warnung')
# button = types.InlineKeyboardButton('Allgemeine Informationen zu Katastrophen', callback_data='allg_infos')
# markup.add(button)

# bot.send_message(chat_id='6475480143',text=startnachricht, reply_markup=markup)

# # Command Handler
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.InlineKeyboardMarkup()
#     button = types.InlineKeyboardButton('Aktuelle Informationen zu Warnungen', callback_data='api_warnung')

#     markup.add(button)

#     bot.send_message(message.chat.id, 'Hallo! Klicke auf den Button:', reply_markup=markup)

# # Nachricht erkennen
# @bot.callback_query_handler(func=lambda call: True)
# def callback_handler(call):
#     # Antworten wenn API Infos gefordert
#     if call.data == 'api_warnung':
#         bot.send_message(call.message.chat.id, 'Antworten zu aktuellen Informationen:')
#     if call.data == 'allg_infos': 
#         bot.send_message(call.message.chat.id, 'Antworten zu allgemeinen Informationen:')

# # Get_Message
# @bot.message_handler(func=lambda message: True)
# def get_Message(message):
# 	#bot.reply_to(message, message.text)
# 	frage = message.text
# 	print(frage)

# # Bot starten 
# bot.infinity_polling()