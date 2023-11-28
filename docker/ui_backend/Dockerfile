#alpine geht nicht zu downloades???
FROM nginx:latest

#index.html in nginx-Verzeichnis kopieren
COPY index.html /usr/share/nginx/html/

WORKDIR usr/src/app

COPY chatbot.py .

CMD ["python", "chatbot.py"]

EXPOSE 80