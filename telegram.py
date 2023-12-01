# import telebot
from telebot import types
import asyncio

from telebot.async_telebot import AsyncTeleBot

# from Warning import *


#### Julian neu #####

with open("token.txt") as file:
    token = file.read()
bot = AsyncTeleBot(token)

async def send_status_message(message):
    status_message = (
       "Hallo! Willkommen beim KatHelferPro Chatbot! Ich bin Rene. Hier gibt es Informationen zum Zivil- und Katastrophenschutz in Deutschland. Beachte bitte, dass ich Fehler machen kann. Prüfe daher Wichtiges nochmal nach."
        " Frag mich nach allgemeinen Informationen zum Katastrophenschutz, Tipps zur Vorsorge, Verhalten bei verschiedenen Katastrophen und wie du dich (auch) langfristig bei verschiedenen Organisationen engagieren kannst. Aktuelle Pegelstände der Gewässer stehen ebenfalls zur Verfügung."
        " Sicherheit geht vor! 🚨"

        "                                                                        Impressum Platzhalter"
    )
    button_akt_Meldung = types.InlineKeyboardButton('Aktuelle Meldungen zum Wetter', callback_data='akt_Meldung')
    button_allg = types.InlineKeyboardButton('Allgemeine Informationen zum Katastrophenschutz', callback_data='allg')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_allg)
    keyboard.add(button_akt_Meldung)

    await bot.reply_to(message, text=status_message, reply_markup=keyboard)
    

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await send_status_message(message.chat.id)

@bot.message_handler(content_types=['new_chat_members'])
async def send_welcome_new_members(message):
    for member in message.new_chat_members:
        if member.id == bot.get_me().id:
            await send_status_message(message.chat.id)



# @bot.message_handler(commands=['start'])
# async def handle_start(message):
#     #print(message)
    

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
    antwort = "Okay, um welche Region handelt es sich? "
    await bot.send_message(message, antwort)



@bot.message_handler(func=lambda message: True)
async def get_Message(message):

    match bot.get_updates().last_update.message:
        case "Okay, um welche Region handelt es sich?":
        # Pauls Code --> Api abruf
            if Ort  gefunden
                antwort = "####################"
                await bot.send_message(message, antwort)
            else:
                await bot.send_message(message, "Zu diesem Ort haben wir keine Meldungen. Probiere es mit einem anderen. Oder tippe \start um etwas anderes zu fragen.")
        case "Zu diesem Ort haben wir keine Meldungen. Probiere es mit einem anderen. Oder tippe \start um etwas anderes zu fragen.":
            if Ort  gefunden
                antwort = "####################"
                await bot.send_message(message, antwort)
            else:
                await bot.send_message(message, "Zu diesem Ort haben wir keine Meldungen. Probiere es mit einem anderen. Oder tippe \start um etwas anderes zu fragen.")
        case _:
            await bot.send_message(message, message.text)

    frage = message.text
    
    await bot.reply_to(message, frage)




asyncio.run(bot.polling())




