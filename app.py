import streamlit as st
from fpdf import FPDF
import base64

st.set_page_config(page_title="Idraulica Rossi AI", page_icon="🔧")

st.title("🔧 Preventivatore Rapido")

with st.form("preventivo_form"):
    cliente = st.text_input("Nome del Cliente")
    tipo = st.selectbox("Tipo Intervento", ["Riparazione", "Installazione", "Manutenzione"])
    ore = st.number_input("Ore di lavoro stimate", min_value=1, step=1)
    materiali = st.number_input("Costo materiali (Euro)", min_value=0.0)
    submit = st.form_submit_button("Calcola e Genera PDF")

if submit:
    prezzo_ora = 40
    imponibile = (ore * prezzo_ora) + materiali
    iva = imponibile * 0.22
    totale = imponibile + iva
    
    st.success(f"### Totale Ivato: Euro {totale:.2f}")

    # Creazione PDF (usiamo 'latin-1' per evitare errori di simboli)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="PREVENTIVO LAVORO", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Intervento: {tipo}", ln=True)
    pdf.ln(5)
    # Abbiamo tolto il simbolo € che rompeva il codice
    pdf.cell(200, 10, txt=f"Ore lavoro: {ore} (Tariffa: Euro {prezzo_ora}/ora)", ln=True)
    pdf.cell(200, 10, txt=f"Costo Materiali: Euro {materiali:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"IVA (22%): Euro {iva:.2f}", ln=True)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt=f"TOTALE FINALE: Euro {totale:.2f}", ln=True)

    # Output del PDF sicuro
    pdf_bytes = pdf.output() # Ritorna byte string di default nelle versioni recenti
    
    # Bottone di scaricamento integrato in Streamlit (più moderno)
    st.download_button(
        label="📥 Scarica il Preventivo PDF",
        data=pdf_bytes,
        file_name=f"preventivo_{cliente}.pdf",
        mime="application/pdf"
    )
    
    st.info("Dopo aver scaricato il PDF, puoi inviarlo direttamente al cliente via WhatsApp o Email.")
