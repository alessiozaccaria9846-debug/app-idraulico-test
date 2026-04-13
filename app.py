import streamlit as st

st.set_page_config(page_title="Idraulica Rossi AI", page_icon="🔧")

st.title("🔧 Preventivatore Rapido")
st.subheader("Configura l'intervento")

with st.form("preventivo_form"):
    cliente = st.text_input("Nome del Cliente")
    tipo = st.selectbox("Tipo Intervento", ["Riparazione", "Installazione", "Manutenzione"])
    ore = st.number_input("Ore di lavoro stimate", min_value=1, step=1)
    materiali = st.number_input("Costo materiali (€)", min_value=0.0)
    
    submit = st.form_submit_button("Calcola Totale")

if submit:
    prezzo_ora = 40
    imponibile = (ore * prezzo_ora) + materiali
    totale = imponibile * 1.22
    
    st.success(f"### Totale Ivato: €{totale:.2f}")
    
    riepilogo = f"Ciao {cliente}, per l'intervento di {tipo} il preventivo stimato è di €{totale:.2f} (IVA inclusa)."
    st.code(riepilogo)
    st.info("Copia il testo sopra e invialo al cliente.")
