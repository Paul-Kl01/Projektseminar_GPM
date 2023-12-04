FROM python:3.11.6-alpine
WORKDIR usr/src/app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "landing.py", "--server.port", "8080"]


