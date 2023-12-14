import streamlit as st
from datetime import datetime
import pandas as pd
from pathlib import Path
import os
from backend.telegram import *



st.set_page_config(
    page_title="Startseite",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.markdown("# Startseite :elephant:")


# Header
header = st.title("Startseite :elephant:")

# Telebot starten
telegram = Telegram()


# weiteren Content hinzufügen
   







