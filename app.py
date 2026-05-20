import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import feedparser
import urllib.parse
import traceback # Ajout pour un meilleur debug

# [Le reste de votre configuration CSS reste inchangé...]
st.set_page_config(page_title="Alpha Terminal Pro | Institutionnel", layout="wide")

# ... (gardez vos fonctions get_fx_rate, safe_float, safe_str, format_metric, etc.)

# ==============================================================================
# CORRECTION : FONCTION DE RÉCUPÉRATION ROBUSTE
# ==============================================================================
def get_safe_ticker_info(ticker_symbol):
    try:
        tk = yf.Ticker(ticker_symbol)
        info = tk.info
        # Vérification si le dictionnaire info contient le minimum vital
        if not info or 'symbol' not in info:
            # Essai de secours : parfois info est vide mais history fonctionne
            hist = tk.history(period="1d")
            if hist.empty:
                return None
            return {'symbol': ticker_symbol, 'longName': ticker_symbol, 'currentPrice': hist['Close'].iloc[-1], 'currency': 'USD'}
        return info
    except Exception:
        return None

# ==============================================================================
# INTERFACE PRINCIPALE (MODIFIÉE)
# ==============================================================================
mode = st.sidebar.radio("Navigation", ["🔍 Terminal Quantitatif", "⚖️ Comparateur Matrice"])

if mode == "🔍 Terminal Quantitatif":
    ticker_input = st.text_input("Recherche", placeholder="Ex: AAPL").upper().strip()
    
    if ticker_input:
        with st.spinner("Analyse en cours..."):
            info = get_safe_ticker_info(ticker_input)
            
            if info is None:
                st.error(f"Impossible de récupérer les données pour '{ticker_input}'. Vérifiez le ticker.")
            else:
                try:
                    # Votre logique d'affichage ici...
                    nom = info.get('longName', ticker_input)
                    st.write(f"## {nom}")
                    # ... (Suite de votre code)
                except Exception as e:
                    st.error("Erreur critique lors de l'affichage :")
                    st.code(traceback.format_exc()) # Affiche l'erreur exacte pour vous
