import streamlit as st
import tempfile
import whisper
from datetime import datetime
import requests
import json
import time
import qrcode
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Generatore Verbale", layout="centered")
st.title("🔒 Login Utente")

# Login iniziale
email = st.text_input("Email", value="1")
licenza = st.text_input("Codice Licenza", type="password", value="1")

# Simulazione check online finto
utenti_autorizzati = {
    "utente@email.com": "ABC123",
    "demo@azienda.it": "DEMO2024",
    "1": "1"
}

# Funzione per ottenere link pubblico da Ngrok
@st.cache_data(show_spinner=False)
def get_ngrok_url():
    try:
        time.sleep(1)  # attesa breve per sincronizzazione con avvio ngrok
        response = requests.get("http://localhost:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                return tunnel["public_url"]
    except Exception as e:
        return "Ngrok non attivo o in avvio..."

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

if email and licenza:
    if email in utenti_autorizzati and utenti_autorizzati[email] == licenza:
        st.success("✅ Accesso autorizzato. Benvenuto!")

        st.title("📝 Generatore di Verbali Aziendali da Audio")

        # Mostra link pubblico generato da ngrok
        ngrok_url = get_ngrok_url()
        if ngrok_url and ngrok_url.startswith("http"):
            st.markdown(f"🌍 **Accesso remoto pubblico:** [{ngrok_url}]({ngrok_url})")
            st.code(ngrok_url, language='text')
            st.image(generate_qr_code(ngrok_url), caption="Scansiona con il telefono", use_column_width=False)
        else:
            st.warning(ngrok_url)

        # Upload file audio
        uploaded_file = st.file_uploader("Carica un file audio", type=["mp3", "wav", "m4a"])

        if uploaded_file is not None:
            st.audio(uploaded_file)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(uploaded_file.read())
                temp_audio_path = tmp.name

            with st.spinner("⏳ Trascrizione in corso..."):
                model = whisper.load_model("base")
                result = model.transcribe(temp_audio_path, language="it")
                trascrizione = result["text"]

            st.success("✅ Trascrizione completata!")

            st.subheader("📄 Testo trascritto:")
            st.text_area("Trascrizione", trascrizione, height=300)

            # Genera verbale
            oggi = datetime.now().strftime("%d/%m/%Y")
            verbale = f"""
VERBALE DI INCONTRO
Data: {oggi}
Luogo: Da specificare

Partecipanti:
- Relatore 1
- Relatore 2

Contenuto della riunione:
{trascrizione}

Conclusione:
- [Sintesi automatica o da completare]
"""

            st.subheader("📑 Verbale Generato:")
            st.text_area("Verbale", verbale, height=400)

            st.download_button("📥 Scarica verbale in .txt", data=verbale, file_name="verbale.txt")

    else:
        st.error("❌ Accesso negato. Email o codice non validi.")
