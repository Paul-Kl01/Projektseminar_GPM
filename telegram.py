## Imports ##
from telebot import types
import asyncio
from telebot.async_telebot import AsyncTeleBot
from backend.Warning import *
from backend.llm import get_llm_answer
import os

# Return none
class Telegram: 
    def __init__(self):
        self.last_message = ""
        self.gesuchte_zeile = Warning()   

        # Token laden über private Variable in Hugging face
        # Der Token muss über die Settings als System-Variable eingebunden werden und entsprechend benannt werden 
        
        # self.bot = AsyncTeleBot(os.environ['Rene_Telegram_Token'])
        # print("Telegram-Bot geladen")


        # Alternativ könnte man auch eine token.txt mit dem Token ablegen
        with open("token.txt") as file:
            token = file.read()
    
        #aktivieren des Bots
        self.start_polling()

    # Funktion zum senden der Startnachricht
    async def send_status_message(self, message):
        status_message = (
        "Hallo! Willkommen beim KatHelferPro Chatbot! Ich bin Rene. Hier gibt es Informationen zum Zivil- und Katastrophenschutz in Deutschland. Beachte bitte, dass ich Fehler machen kann. Prüfe daher Wichtiges nochmal nach. \n"
            " Frag mich nach allgemeinen Informationen zum Katastrophenschutz, Tipps zur Vorsorge, Verhalten bei verschiedenen Katastrophen und wie du dich (auch) langfristig bei verschiedenen Organisationen engagieren kannst. Aktuelle Meldungen stehen ebenfalls zur Verfügung. \n"
            " Sicherheit geht vor! 🚨 \n"

            "                                                                        Impressum Platzhalter"
        )
        button_akt_Meldung = types.InlineKeyboardButton('Aktuelle Warnungen', callback_data='akt_Meldung')
        button_allg = types.InlineKeyboardButton('Allgemeine Informationen zum Katastrophenschutz', callback_data='allg')

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_allg)
        keyboard.add(button_akt_Meldung)

        last_message = status_message
        await self.bot.reply_to(message, text=status_message, reply_markup=keyboard)

    # Message Handler
    def start_polling(self):
        # handeln des /start Befehls
        @self.bot.message_handler(commands=['start'])
        async def send_welcome(message):
            await self.send_status_message(message)

        # automatisiertes ausführen des /start Befehls beim ersten öffnen des Chats
        @self.bot.message_handler(content_types=['new_chat_members'])
        async def send_welcome_new_members(message):
            for member in message.new_chat_members:
                if member.id == self.bot.get_me().id:
                    await self.send_status_message(message.chat.id)
        

        # Button-Handler
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

        # Chat-Story Steuerung
        @self.bot.message_handler(func=lambda message: True)
        async def get_Message(message):
            match self.last_message:
                # Reaktion auf die Auswahl: aktuelle Meldungen
                case "Okay, um welchen Ort handelt es sich?":
                    ort = message.text
                    # Bestimmen der Warnmeldungen für einen Ort und Rückgabe
                    antwort = self.gesuchte_zeile.getWarningOrt(ort)
                    
                    if antwort == "Keine Warnung gefunden":
                        erw_ant = "Zu diesem Ort haben wir keine Meldungen. \nProbiere es mit einem anderen. Oder tippe /start, um etwas anderes zu fragen."
                        self.last_message = "Okay, um welchen Ort handelt es sich?"
                        await self.bot.send_message(message.chat.id, erw_ant)
                    else:
                        erw_ant = "Wir haben zu diesem Ort folgende Meldungen: \n" + antwort +  "\n\nSuche nach einem neuen Ort oder tippe /start, um etwas anderes zu fragen."
                        self.last_message = "Okay, um welchen Ort handelt es sich?"
                        await self.bot.send_message(message.chat.id, erw_ant)

                # Reaktion auf die Auswahl: allgemeine Informationen
                case "Okay, es geht um allgemeine Informationen zum Katastrophenschutz. Stelle mir einfach eine Frage und ich gebe mein Bestes, um dir weiterzuhelfen!":
                    self.last_message = "Okay, es geht um allgemeine Informationen zum Katastrophenschutz. Stelle mir einfach eine Frage und ich gebe mein Bestes, um dir weiterzuhelfen!"
                    # Übergabe der Frage an das LLM und bestimmen der Antwort
                    erw_ant = get_llm_answer(message.text) + " \n \nUm weitere Antworten zu erhalten, stelle mir gerne noch eine Frage oder tippe /start, um aktuelle Meldungen zu erhalten."
                    await self.bot.send_message(message.chat.id, erw_ant)

                #Fehlermeldung
                case _:
                    self.last_message = "Bitte starte den Bot mit /start neu."
                    await self.bot.send_message(message.chat.id, self.last_message)
                    
        #aufrechterhalten der Schleife
        asyncio.run(self.bot.polling())

    # Textausgabe nach Auswahl eines Buttons
    async def function_allg(self, message):
        antwort = "Okay, es geht um allgemeine Informationen zum Katastrophenschutz. Stelle mir einfach eine Frage und ich gebe mein Bestes, um dir weiterzuhelfen!"
        self.last_message = antwort
        await self.bot.send_message(message.chat.id, antwort)

    async def function_akt_meldungen(self, message):
        antwort = "Okay, um welchen Ort handelt es sich?"
        self.last_message = antwort
        await self.bot.send_message(message.chat.id, antwort)
