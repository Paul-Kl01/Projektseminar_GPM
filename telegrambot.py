import requests
import json
import time
import subprocess # ausführen von .sh aus Programm
import os

with open("token.txt") as file:
    token = file.read()

def incoming():
    global count1
    answer = requests.get(f"https://api.telegram.org/bot{token}/getUpdates")
    data = json.loads(answer.content) 
    text = [item['message']['text'] for item in data['result']] #gibt ein Array mit den Texten zurück
    return text

def sendMessage(text):
    params = {"chat_id":"5342193739", "text":f"{text}"}
    url = f"https://api.telegram.org/bot{token}/sendMessage"    #f brauch es damit {token} als Variable erkannt wird
    message = requests.post(url, params=params)