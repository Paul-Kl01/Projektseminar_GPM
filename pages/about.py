import streamlit as st
from transformers import pipeline
import datetime
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Impressum",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Titel
st.markdown("# Impressum")
st.sidebar.markdown("# Impressum")

# weiteren Content, Impressum etc. hinzufügen
