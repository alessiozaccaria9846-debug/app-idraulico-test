import streamlit as st
from fpdf import FPDF

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
    pdf.cell(200, 10, txt=f"Ore lavoro: {ore} (Tariffa: Euro {prezzo_ora}/ora)", ln=True)
    pdf.cell(200, 10, txt=f"Costo Materiali: Euro {materiali:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"IVA (22%): Euro {iva:.2f}", ln=True)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt=f"TOTALE FINALE: Euro {totale:.2f}", ln=True)

    # TRUCCO PER RISOLVERE L'ERRORE: Trasformiamo il PDF in byte puri
    pdf_bytes = pdf.output()
    if isinstance(pdf_bytes, str): # Gestione versioni diverse della libreria
        pdf_bytes = pdf_bytes.encode('latin-1')

    # Bottone di scaricamento
    st.download_button(
        label="📥 Scarica il Preventivo PDF",
        data=bytes(pdf_bytes), # Lo forziamo in formato 'bytes'
        file_name=f"preventivo_{cliente.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
    
    st.info("Tocca il tasto sopra per scaricare il file sul telefono.")
