import streamlit as st
from fpdf import FPDF

# 1. Configurazione pagina
st.set_page_config(page_title="Gestione Preventivi AI", page_icon="🔧")

# 2. Codice CSS per nascondere menu, footer e tasto Deploy di Streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Interfaccia Utente
st.title("🔧 Preventivatore Rapido")
st.write("Inserisci i dati per generare il preventivo professionale in PDF.")

with st.form("preventivo_form"):
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Nome del Cliente")
        tipo = st.selectbox("Tipo Intervento", ["Riparazione", "Installazione", "Manutenzione", "Sopralluogo"])
    with col2:
        ore = st.number_input("Ore di lavoro stimate", min_value=1, step=1)
        materiali = st.number_input("Costo materiali (Euro)", min_value=0.0)
    
    submit = st.form_submit_button("Calcola e Genera PDF")

# 4. Logica di calcolo e generazione PDF
if submit:
    if not cliente:
        st.error("Per favore, inserisci il nome del cliente.")
    else:
        prezzo_ora = 40
        imponibile = (ore * prezzo_ora) + materiali
        iva = imponibile * 0.22
        totale = imponibile + iva
        
        st.success(f"### Totale Stimato: Euro {totale:.2f}")

        # Creazione documento PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Intestazione
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="PREVENTIVO DI LAVORO", ln=True, align='C')
        pdf.ln(10)
        
        # Dettagli Cliente e Intervento
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
        pdf.cell(200, 10, txt=f"Tipo di Intervento: {tipo}", ln=True)
        pdf.ln(5)
        
        # Tabella Costi
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        pdf.cell(200, 10, txt=f"Manodopera ({ore} ore x Euro {prezzo_ora}/ora): Euro {ore * prezzo_ora:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Materiali e Ricambi: Euro {materiali:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"IVA (22%): Euro {iva:.2f}", ln=True)
        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        # Totale
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, txt=f"TOTALE FINALE: Euro {totale:.2f}", ln=True)
        
        # Trasformazione in byte per il download
        pdf_bytes = pdf.output()
        if isinstance(pdf_bytes, str):
            pdf_bytes = pdf_bytes.encode('latin-1')

        # Tasto di download
        st.download_button(
            label="📥 Scarica il Preventivo PDF",
            data=bytes(pdf_bytes),
            file_name=f"preventivo_{cliente.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
        
        st.info("Consiglio: Una volta scaricato, invialo subito al cliente via WhatsApp!")
