# import telebot
from telebot import types
import asyncio
from telebot.async_telebot import AsyncTeleBot
from Warning import *
import os 

class Telegram: 
    def __init__(self):
        self.last_message = ""
        self.gesuchte_zeile = Warning()    
        
        # Token laden über private Variable in Hugging face
        #  der Token muss über die Settings als System-Variable eingebunden werden und entsprechend benannt werden 
        # self.bot = AsyncTeleBot(os.environ['BotToken'])
        #  print("Telegram-Bot geladen")

        #Token laden über token.txt
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
                    ort = message.text
                    antwort = self.gesuchte_zeile.getWarningOrt(ort)
                    
                    if antwort == "Keine Warnung gefunden":
                        erw_ant = "Zu diesem Ort haben wir keine Meldungen. Probiere es mit einem anderen. Oder tippe /start um etwas anderes zu fragen."
                        self.last_message = "Okay, um welche Region handelt es sich?"
                        await self.bot.send_message(message.chat.id, erw_ant)
                    else:
                        erw_ant = "Wir haben zu diesem Ort folgende Meldungen: \n" + antwort +  "\nSuche nach einem neuen ort oder tippe /start um etwas anderes zu fragen."
                        self.last_message = "Okay, um welche Region handelt es sich?"
                        await self.bot.send_message(message.chat.id, erw_ant)
                case "Okay, es geht um allgemeine Informationen zum Katastrophenschutz. Stelle mir einfach eine Frage und ich gebe mein Bestes, um dir weiterzuhelfen!":
                    ######zauberei einfügen#####
                    self.last_message = "Okay, es geht um allgemeine Informationen zum Katastrophenschutz. Stelle mir einfach eine Frage und ich gebe mein Bestes, um dir weiterzuhelfen!"
                    erw_ant = "🚨Zauberei soll kommen puff peng...konfetti!!!🚨"
                    await self.bot.send_message(message.chat.id, erw_ant)        
                case _:
                    self.last_message = "Bitte starte den Bot mit /start neu."
                    await self.bot.send_message(message.chat.id, self.last_message)
        asyncio.run(self.bot.polling())

    async def function_allg(self, message):
        antwort = "Okay, es geht um allgemeine Informationen zum Katastrophenschutz. Stelle mir einfach eine Frage und ich gebe mein Bestes, um dir weiterzuhelfen!"
        self.last_message = antwort
        await self.bot.send_message(message.chat.id, antwort)

    async def function_akt_meldungen(self, message):
        antwort = "Okay, um welche Region handelt es sich?"
        self.last_message = antwort
        await self.bot.send_message(message.chat.id, antwort)

telegram = Telegram()
telegram.start_polling()
