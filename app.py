import streamlit as st
from fpdf import FPDF

# 1. Configurazione pagina (Personalizziamo l'icona e il titolo della scheda)
st.set_page_config(page_title="Gestionale Artigiani", page_icon="🔧", layout="centered")

# 2. CSS AGGIORNATO: Questo toglie TUTTO (barra in alto, footer, e pulsanti di gestione)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Nasconde il pulsante rosso "Deploy" e la toolbar di amministrazione */
            .stAppDeployButton {display:none;}
            .st-emotion-cache-18ni7ve {display: none;}
            [data-testid="stToolbar"] {visibility: hidden !important;}
            [data-testid="stDecoration"] {display: none;}
            /* Toglie lo spazio bianco in alto che resta dopo aver tolto l'header */
            .block-container {padding-top: 1rem;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- DA QUI IN POI IL RESTO DEL CODICE RESTA UGUALE ---

st.title("🔧 Preventivatore Rapido")
st.write("Genera il tuo PDF professionale in un click.")

with st.form("preventivo_form"):
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Nome del Cliente")
        tipo = st.selectbox("Tipo Intervento", ["Riparazione", "Installazione", "Manutenzione"])
    with col2:
        ore = st.number_input("Ore di lavoro stimate", min_value=1, step=1)
        materiali = st.number_input("Costo materiali (Euro)", min_value=0.0)
    
    # Personalizziamo il colore del tasto con una colonna per farlo risaltare
    submit = st.form_submit_button("CALCOLA E GENERA PDF")

if submit:
    if not cliente:
        st.error("Inserisci il nome del cliente!")
    else:
        prezzo_ora = 40
        imponibile = (ore * prezzo_ora) + materiali
        iva = imponibile * 0.22
        totale = imponibile + iva
        
        st.success(f"### Totale: Euro {totale:.2f}")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="PREVENTIVO LAVORO", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
        pdf.cell(200, 10, txt=f"Intervento: {tipo}", ln=True)
        pdf.ln(5)
        pdf.cell(200, 10, txt=f"Manodopera: Euro {ore * prezzo_ora:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Materiali: Euro {materiali:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"IVA (22%): Euro {iva:.2f}", ln=True)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, txt=f"TOTALE FINALE: Euro {totale:.2f}", ln=True)

        pdf_bytes = pdf.output()
        if isinstance(pdf_bytes, str):
            pdf_bytes = pdf_bytes.encode('latin-1')

        st.download_button(
            label="📥 SCARICA IL PREVENTIVO PDF",
            data=bytes(pdf_bytes),
            file_name=f"preventivo_{cliente.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
