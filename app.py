import streamlit as st
import tempfile
from datetime import datetime
import qrcode
from io import BytesIO
from PIL import Image
import os
import shutil

st.set_page_config(page_title="Generatore Verbale", layout="wide")

# Layout desktop minimale con larghezza estesa
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    .stTextInput > div > input {
        font-size: 16px;
    }
    .stButton > button {
        font-size: 16px;
        padding: 0.5rem 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔒 Login Utente")

# Login iniziale (manteniamo utente demo per test manuale)
email = st.text_input("Email")
licenza = st.text_input("Codice Licenza", type="password")

# Simulazione check online finto
utenti_autorizzati = {
    "utente@email.com": "ABC123",
    "demo@azienda.it": "DEMO2024",
    "1": "1"
}

# Funzione per generare QR Code
def generate_qr_code(link):
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return Image.open(buf)

# Dominio statico (sostituire con il proprio se diverso)
ngrok_url = "https://smartverbale.ngrok-free.app"

# Cartella per backup audio
BACKUP_DIR = "audio_backup"
os.makedirs(BACKUP_DIR, exist_ok=True)

if email and licenza:
    if email in utenti_autorizzati and utenti_autorizzati[email] == licenza:
        st.success("✅ Accesso autorizzato. Benvenuto!")

        st.title("📝 Generatore di Verbali Aziendali da Audio")

        # Mostra link pubblico statico + QR
        st.markdown(f"🌍 **Accesso remoto pubblico:** [{ngrok_url}]({ngrok_url})")
        st.code(ngrok_url, language='text')
        st.image(generate_qr_code(ngrok_url), caption="Scansiona con il telefono", use_column_width=False)

        # Upload file audio
        uploaded_file = st.file_uploader("Carica un file audio", type=["mp3", "wav", "m4a"])

        if uploaded_file is not None:
            st.audio(uploaded_file)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(uploaded_file.read())
                temp_audio_path = tmp.name

            # Salva il file nella cartella di backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(BACKUP_DIR, f"audio_{timestamp}.wav")
            shutil.copy(temp_audio_path, backup_path)

            st.success("✅ File ricevuto e salvato come backup!")
            st.warning("⚠️ Questo server non elabora l'audio. Carica il file su una postazione abilitata alla trascrizione.")

            st.info(f"📁 Backup salvato in: {backup_path}")

        # Mostra i file salvati nella cartella di backup
        st.subheader("📂 File audio salvati:")
        backup_files = sorted(os.listdir(BACKUP_DIR), reverse=True)
        for file_name in backup_files:
            file_path = os.path.join(BACKUP_DIR, file_name)
            with open(file_path, "rb") as f:
                st.download_button(label=f"📥 Scarica {file_name}", data=f, file_name=file_name)

    else:
        st.error("❌ Accesso negato. Email o codice non validi.")
