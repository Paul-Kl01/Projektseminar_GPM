# import telebot
# from telebot import types
import asyncio
from telebot.async_telebot import AsyncTeleBot

from Warning import *


#### Julian neu #####

with open("token.txt") as file:
    token = file.read()
bot = AsyncTeleBot(token)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
            Hi there, I am EchoBot.
            I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
            """)

@bot.message_handler(func=lambda message: True)
async def get_Message(message):
    frage = message.text
    print(frage)
    
    # Warnung für genannten Ort abfragen 
    gesuchte_zeile = Warning(frage).getWarningOrt()
    
    # Bot Repy mit Warnung 
    await bot.reply_to(message, gesuchte_zeile)

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