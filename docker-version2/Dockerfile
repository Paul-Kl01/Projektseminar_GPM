FROM python:3.11.6-alpine

WORKDIR usr/src/app

COPY chatbot.py .

#Abhängigkeiten müssen je nach dem was in der App gebraucht wird installiert werden

CMD ["python", "chatbot.py", "--host", "0.0.0.0", "--port", "7860"]
