import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
from datetime import datetime

# Design der Webseite einstellen
st.set_page_config(page_title="Stempeluhr", layout="centered")

st.title("⏱️ Digitale Stempeluhr")

try:
    # 1. Verbindung im Hintergrund herstellen
    secret_str = st.secrets["gcp_service_account"]
    creds_dict = json.loads(secret_str)
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    
    # Tabelle über deine URL öffnen
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1siXS3m36SuPVi1bRHXMDA2Oun6jMeNFmIy3FvzHXQ1o/edit?pli=1&gid=0#gid=0")
    stammdaten = sheet.worksheet("Stammdaten").get_all_records()
    
    st.write("---") # Visuelle Trennlinie
    
    # 2. Das Terminal für die Mitarbeiter bauen
    # Wir filtern die Excel-Tabelle so, dass nur Leute angezeigt werden, bei denen Status "aktiv" steht
    aktive_mitarbeiter = []
    for m in stammdaten:
        if str(m.get('Status', '')).lower() == 'aktiv':
            aktive_mitarbeiter.append(f"{m['Mitarbeiter_ID']} - {m['Vorname']} {m['Nachname']}")
            
    if aktive_mitarbeiter:
        # Dropdown Menü
        gewaehlter_ma = st.selectbox("Wer stempelt gerade?", aktive_mitarbeiter)
        
        st.write("") # Ein bisschen Platz lassen
        
        # Zwei Spalten für die Buttons nebeneinander erstellen
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🟢 KOMMEN (Arbeitsbeginn)", use_container_width=True):
                jetzt = datetime.now().strftime("%H:%M:%S")
                st.success(f"Guten Schichtbeginn! Erfasst um {jetzt} Uhr.")
        with col2:
            if st.button("🔴 GEHEN (Feierabend)", use_container_width=True):
                jetzt = datetime.now().strftime("%H:%M:%S")
                st.success(f"Schönen Feierabend! Erfasst um {jetzt} Uhr.")
    else:
        st.warning("Keine aktiven Mitarbeiter in der Datenbank gefunden.")

    st.write("---")
    
    # 3. Den alten Tabellen-Check verstecken wir in einem Admin-Bereich
    with st.expander("🛠️ Admin-Bereich: Stammdaten einsehen"):
        st.dataframe(stammdaten)

except Exception as e:
    st.error("❌ Fehler bei der Verbindung.")
    st.info("Grund: " + str(e))
