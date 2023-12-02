# import telebot
from telebot import types
import asyncio
from telebot.async_telebot import AsyncTeleBot
from Warning import *

class Telegram: 
    def __init__(self):
        self.last_message = ""
        self.gesuchte_zeile = Warning()    

        with open("token.txt") as file:
            token = file.read()
    
        self.bot = AsyncTeleBot(token)
    
    async def send_status_message(self, message):
        status_message = (
        "Hallo! Willkommen beim KatHelferPro Chatbot! Ich bin Rene. Hier gibt es Informationen zum Zivil- und Katastrophenschutz in Deutschland. Beachte bitte, dass ich Fehler machen kann. Prüfe daher Wichtiges nochmal nach."
            " Frag mich nach allgemeinen Informationen zum Katastrophenschutz, Tipps zur Vorsorge, Verhalten bei verschiedenen Katastrophen und wie du dich (auch) langfristig bei verschiedenen Organisationen engagieren kannst. Aktuelle Pegelstände der Gewässer stehen ebenfalls zur Verfügung."
            " Sicherheit geht vor! 🚨"

            "                                                                        Impressum Platzhalter"
        )
        button_akt_Meldung = types.InlineKeyboardButton('Aktuelle Warnungen', callback_data='akt_Meldung')
        button_allg = types.InlineKeyboardButton('Allgemeine Informationen zum Katastrophenschutz', callback_data='allg')

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_allg)
        keyboard.add(button_akt_Meldung)

        last_message = status_message
        await self.bot.reply_to(message, text=status_message, reply_markup=keyboard)
        
    def start_polling(self):
        @self.bot.message_handler(commands=['start'])
        async def send_welcome(message):
            await self.send_status_message(message)

        @self.bot.message_handler(content_types=['new_chat_members'])
        async def send_welcome_new_members(message):
            for member in message.new_chat_members:
                if member.id == self.bot.get_me().id:
                    await self.send_status_message(message.chat.id)
        

        @self.bot.callback_query_handler(func=lambda call: True)
        async def handle_button_click(call):
            match call.data:
                case "allg":
                    # Hier wird die Funktion aufgerufen, die du mit Button 1 verknüpfen möchtest
                    print("Call: ") 
                    print(call)
                    print("Data: ") 
                    print(call.data)
                    print("MSg: ") 
                    print(call.message)
                    await self.function_allg(call.message)
                case "akt_Meldung":
                    # Hier wird die Funktion aufgerufen, die du mit Button 1 verknüpfen möchtest
                    await self.function_akt_meldungen(call.message)

                case _:
                    # Hier wird die Funktion aufgerufen, die du mit Button 2 verknüpfen möchtest
                    last_message = "Der Button ist nicht angebunden."
                    await self.send_message(call.message.chat.id, last_message)
                    
        @self.bot.message_handler(func=lambda message: True)
        async def get_Message(message):
            match self.last_message:
                case "Okay, um welche Region handelt es sich?":
                # Pauls APi abruf
                    print(message.text)
                    ort = message.text
                    print(ort)
                    antwort = self.gesuchte_zeile.getWarningOrt(ort)
                    
                    if antwort == "Keine Warnung gefunden":
                        self.last_message = "Zu diesem Ort haben wir keine Meldungen. Probiere es mit einem anderen. Oder tippe \start um etwas anderes zu fragen."
                        await self.bot.send_message(message.chat.id, self.last_message)
                    else:
                        erw_ant = "Wir haben zu diesem Ort folgende Meldungen: \n" + antwort +  "\n Tippe \start um etwas anderes zu fragen."
                        self.last_message = antwort
                        await self.bot.send_message(message.chat.id, erw_ant)
                case "Zu diesem Ort haben wir keine Meldungen. Probiere es mit einem anderen. Oder tippe \start um etwas anderes zu fragen.":
                    ort = message.text
                    antwort = self.bot.gesuchte_zeile.getWarningOrt(ort)
                    if antwort == "Keine Warnung gefunden":
                        self.last_message = "Zu diesem Ort haben wir keine Meldungen. Probiere es mit einem anderen. Oder tippe \start um etwas anderes zu fragen."
                        await self.bot.send_message(message.chat.id, self.last_message)
                    else:
                        erw_ant = "Wir haben zu diesem Ort folgende Meldungen: \n" + antwort +  "\n Tippe \start um etwas anderes zu fragen."
                        self.last_message = antwort
                        await self.bot.send_message(message.chat.id, antwort)
                case _:
                    print(self.last_message)
                    self.last_message = "Bitte nutze einen der Buttons. Im Notfall kannst du den Chat mit \start neustarten."
                    await self.bot.send_message(message.chat.id, self.last_message)

            frage = message.text
            
            #await self.bot.reply_to(message, frage)
            
        asyncio.run(self.bot.polling())

    async def function_allg(self, message):
        # hier bitte den Zaubereipart einsenden
        antwort = "Du möchtest allgemeine Informationen"
        self.last_message = antwort
        await self.bot.send_message(message.chat.id, antwort)

    async def function_akt_meldungen(self, message):
        # hier bitte Pauls abfrage einfügen
        antwort = "Okay, um welche Region handelt es sich?"
        self.last_message = antwort
        await self.bot.send_message(message.chat.id, antwort)


telegram = Telegram()
telegram.start_polling()



# # import telebot
# # from telebot import types
# import asyncio
# from telebot.async_telebot import AsyncTeleBot

# from Warning import *


# #### Julian neu #####

# with open("token.txt") as file:
#     token = file.read()
    
# bot = AsyncTeleBot(token)

# gesuchte_zeile = Warning()


# # Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
# async def send_welcome(message):
#     await bot.reply_to(message, """\
#             Hi there, I am EchoBot.
#             I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
#             """)

# @bot.message_handler(func=lambda message: True)
# async def get_Message(message):
#     frage = message.text
#     print(frage)
    
#     # Warnung für genannten Ort abfragen 
#     antw = gesuchte_zeile.getWarningOrt(frage)
    
#     # Bot Repy mit Warnung 
#     await bot.reply_to(message, antw)

# asyncio.run(bot.polling())