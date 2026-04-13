import streamlit as st
from fpdf import FPDF
import base64

st.set_page_config(page_title="Idraulica Rossi AI", page_icon="🔧")

st.title("🔧 Preventivatore Rapido")

with st.form("preventivo_form"):
    cliente = st.text_input("Nome del Cliente")
    tipo = st.selectbox("Tipo Intervento", ["Riparazione", "Installazione", "Manutenzione"])
    ore = st.number_input("Ore di lavoro stimate", min_value=1, step=1)
    materiali = st.number_input("Costo materiali (€)", min_value=0.0)
    submit = st.form_submit_button("Calcola e Genera PDF")

if submit:
    prezzo_ora = 40
    imponibile = (ore * prezzo_ora) + materials
    iva = imponibile * 0.22
    totale = imponibile + iva
    
    st.success(f"### Totale Ivato: €{totale:.2f}")

    # Creazione PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="PREVENTIVO LAVORO", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Intervento: {tipo}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Ore lavoro: {ore} (Tariffa: €{prezzo_ora}/ora)", ln=True)
    pdf.cell(200, 10, txt=f"Costo Materiali: €{materiali:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"IVA (22%): €{iva:.2f}", ln=True)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt=f"TOTALE FINALE: €{totale:.2f}", ln=True)

    # Output del PDF
    pdf_output = pdf.output(dest='S').encode('latin-1')
    b64 = base64.b64encode(pdf_output).decode()
    
    # Bottone di scaricamento
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="preventivo_{cliente}.pdf">📥 Scarica il Preventivo PDF</a>'
    st.markdown(href, unsafe_content_type=True)
    
    st.info("Dopo aver scaricato il PDF, puoi inviarlo direttamente al cliente.")
