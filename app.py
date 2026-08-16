import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="Zeiterfassung", layout="wide")

st.title("⏱️ Zeiterfassungssystem - Dashboard")

# 1. Den unsichtbaren Roboter-Schlüssel aus dem Tresor holen
try:
    secret_str = st.secrets["gcp_service_account"]
    creds_dict = json.loads(secret_str)
    
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    
    # 2. Mit Google Sheets verbinden
    client = gspread.authorize(creds)
    
    # 3. Genau deine Datei öffnen
    # WICHTIG: Der Name hier muss exakt so sein, wie deine Google Sheet Datei heißt!
    sheet = client.open("Backend_Zeiterfassung_KundeA")
    
    # 4. Das Tabellenblatt "Stammdaten" auslesen
    stammdaten = sheet.worksheet("Stammdaten").get_all_records()
    
    st.success("✅ Verbindung zur Datenbank erfolgreich hergestellt!")
    
    st.subheader("Aktuelle Mitarbeiter (Stammdaten)")
    st.dataframe(stammdaten)

except Exception as e:
    st.error("❌ Fehler bei der Verbindung zur Datenbank.")
    st.info("Hier ist der Grund: " + str(e))
