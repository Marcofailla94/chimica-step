   import re
import streamlit as st

from modules.bilanciamento import bilancia_reazione, formula_to_html
from modules.masse import calcola_massa_molecolare
from modules.ai_solver import risolvi_con_ai
from modules.leggi_chimiche import (
    lavoisier_due_reagenti_un_prodotto,
    lavoisier_due_reagenti_due_prodotti,
    proust_trova_massa_secondo_elemento,
    proust_verifica_composto,
    dalton_due_composti
)


def mostra_soluzione_formattata(testo):
    """
    Riconosce i blocchi [LATEX] ... [/LATEX]
    e li mostra come formule pulite.
    """

    pattern = r"\[LATEX\]\s*(.*?)\s*\[/LATEX\]"
    parti = re.split(pattern, testo, flags=re.DOTALL | re.IGNORECASE)

    for i, parte in enumerate(parti):
        if not parte.strip():
            continue

        if i % 2 == 1:
            try:
                st.markdown('<div class="formula-box">', unsafe_allow_html=True)
                st.latex(parte.strip())
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception:
                st.code(parte.strip())
        else:
            st.markdown(parte)


st.set_page_config(
    page_title="Chimica Step",
    page_icon="🧪",
    layout="wide"
)


st.markdown("""
<style>
.main-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #0b5c56;
}
.subtitle {
    font-size: 1.1rem;
    color: #444;
}
.result {
    background-color: #e8f5e9;
    border-left: 6px solid #2e7d32;
    padding: 16px;
    border-radius: 10px;
    margin-bottom: 15px;
}
.formula-box {
    background-color: #f0fdf9;
    border: 2px solid #00a86b;
    border-radius: 12px;
    padding: 18px;
    margin: 15px 0;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title">🧪 Chimica Step</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Risolutore guidato per chimica - primo anno liceo classico</div>',
    unsafe_allow_html=True
)

st.divider()


menu = st.sidebar.radio(
    "Scegli il tipo di esercizio",
    [
        "Home",
        "Risolvi con AI",
        "Bilanciamento reazioni",
        "Legge di Lavoisier",
        "Legge di Proust",
        "Legge di Dalton",
        "Massa molecolare"
    ]
)


if menu == "Home":
    st.header("Benvenuto")

    st.markdown("""
Questa app risolve esercizi di chimica spiegando i passaggi.

È pensata per il primo anno di liceo classico.

Non usa:
- moli;
- numero di Avogadro;
- stechiometria avanzata.
""")

    st.info("Scegli un argomento dal menu a sinistra.")


elif menu == "Risolvi con AI":
    st.header("🤖 Risolvi esercizio con AI")

    st.markdown("""
Incolla qui l'esercizio di chimica.

L'AI risolverà passo passo usando formule e calcoli scritti bene.
""")

    testo_esercizio = st.text_area(
        "Testo dell'esercizio",
        height=250,
        placeholder=(
            "Esempio: L'anidride solforica reagendo con l'acqua forma acido solforico. "
            "Se 80 g di anidride solforica formano 98 g di acido solforico, "
            "calcola la massa di acqua."
        )
    )

    if st.button("Risolvi con AI"):
        if not testo_esercizio.strip():
            st.warning("Scrivi prima l'esercizio.")
        else:
            with st.spinner("Sto risolvendo l'esercizio..."):
                try:
                    soluzione = risolvi_con_ai(testo_esercizio)
                    st.markdown("### Soluzione")
                    mostra_soluzione_formattata(soluzione)
                except Exception as e:
                    st.error(f"Errore: {e}")


elif menu == "Bilanciamento reazioni":
    st.header("⚖️ Bilanciamento reazioni")

    st.markdown("""
Scrivi la reazione usando `->`.

Esempi:
- `Fe + O2 -> Fe2O3`
- `H3PO4 + NaOH -> Na2HPO4 + H2O`
- `Mn(OH)2 + H3PO4 -> Mn3(PO4)2 + H2O`
""")

    reazione = st.text_input(
        "Inserisci la reazione",
        "Fe + O2 -> Fe2O3"
    )

    if st.button("Bilancia"):
        try:
            risultato = bilancia_reazione(reazione)

            st.markdown('<div class="result">', unsafe_allow_html=True)
            st.subheader("Reazione bilanciata")
            st.markdown(risultato["equazione_html"], unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("Passaggi")
            for passo in risultato["passi"]:
                st.write(passo)

            st.subheader("Controllo finale")
            st.dataframe(risultato["tabella"], use_container_width=True)

        except Exception as e:
            st.error(f"Errore: {e}")


elif menu == "Legge di Lavoisier":
    st.header("⚖️ Legge di Lavoisier")

    st.markdown("""
**La legge di Lavoisier dice:**

> La massa totale dei reagenti è uguale alla massa totale dei prodotti.
""")

    tipo = st.radio(
        "Scegli il tipo di esercizio",
        [
            "Due reagenti e un prodotto",
            "Due reagenti e due prodotti"
        ]
    )

    if tipo == "Due reagenti e un prodotto":
        st.subheader("A + B → C")

        col1, col2 = st.columns(2)

        with col1:
            massa_reagente_noto = st.number_input(
                "Massa reagente noto, in grammi",
                value=80.0
            )

            massa_prodotto = st.number_input(
                "Massa prodotto, in grammi",
                value=98.0
            )

        with col2:
            nome_reagente_noto = st.text_input(
                "Nome reagente noto",
                "anidride solforica"
            )

            nome_reagente_incognito = st.text_input(
                "Nome reagente da trovare",
                "acqua"
            )

            nome_prodotto = st.text_input(
                "Nome prodotto",
                "acido solforico"
            )

        if st.button("Risolvi Lavoisier"):
            risultato = lavoisier_due_reagenti_un_prodotto(
                massa_reagente_noto,
                massa_prodotto,
                nome_reagente_noto,
                nome_reagente_incognito,
                nome_prodotto
            )

            st.markdown('<div class="result">', unsafe_allow_html=True)
            st.subheader("Risultato")
            st.write(risultato["risultato"])
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("Passaggi")
            for passo in risultato["passi"]:
                st.write(passo)

    else:
        st.subheader("A + B → C + D")

        col1, col2 = st.columns(2)

        with col1:
            massa_reagente_1 = st.number_input(
                "Massa reagente 1, in grammi",
                value=10.0
            )

            massa_reagente_2 = st.number_input(
                "Massa reagente 2, in grammi",
                value=20.0
            )

            massa_prodotto_noto = st.number_input(
                "Massa prodotto noto, in grammi",
                value=18.0
            )

        with col2:
            nome_reagente_1 = st.text_input(
                "Nome reagente 1",
                "sostanza A"
            )

            nome_reagente_2 = st.text_input(
                "Nome reagente 2",
                "sostanza B"
            )

            nome_prodotto_noto = st.text_input(
                "Nome prodotto noto",
                "sostanza C"
            )

            nome_prodotto_incognito = st.text_input(
                "Nome prodotto da trovare",
                "sostanza D"
            )

        if st.button("Risolvi esercizio"):
            risultato = lavoisier_due_reagenti_due_prodotti(
                massa_reagente_1,
                massa_reagente_2,
                massa_prodotto_noto,
                nome_reagente_1,
                nome_reagente_2,
                nome_prodotto_noto,
                nome_prodotto_incognito
            )

            st.markdown('<div class="result">', unsafe_allow_html=True)
            st.subheader("Risultato")
            st.write(risultato["risultato"])
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("Passaggi")
            for passo in risultato["passi"]:
                st.write(passo)


elif menu == "Legge di Proust":
    st.header("📏 Legge di Proust")

    st.markdown("""
**La legge di Proust dice:**

> In un composto gli elementi sono sempre presenti nello stesso rapporto di massa.
""")

    tipo = st.radio(
        "Scegli il tipo di esercizio",
        [
            "Trova la massa mancante",
            "Verifica se il rapporto è corretto"
        ]
    )

    if tipo == "Trova la massa mancante":
        col1, col2 = st.columns(2)

        with col1:
            massa_elemento_1 = st.number_input(
                "Massa elemento 1, in grammi",
                value=7.0
            )

            rapporto = st.number_input(
                "Rapporto elemento 1 / elemento 2",
                value=3.5
            )

        with col2:
            nome1 = st.text_input("Nome elemento 1", "ferro")
            nome2 = st.text_input("Nome elemento 2", "ossigeno")

        if st.button("Risolvi Proust"):
            risultato = proust_trova_massa_secondo_elemento(
                massa_elemento_1,
                rapporto,
                nome1,
                nome2
            )

            st.markdown('<div class="result">', unsafe_allow_html=True)
            st.subheader("Risultato")
            st.write(risultato["risultato"])
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("Passaggi")
            for passo in risultato["passi"]:
                st.write(passo)

    else:
        col1, col2 = st.columns(2)

        with col1:
            massa_elemento_1 = st.number_input(
                "Massa elemento 1, in grammi",
                value=14.0
            )

            massa_elemento_2 = st.number_input(
                "Massa elemento 2, in grammi",
                value=4.0
            )

            rapporto_corretto = st.number_input(
                "Rapporto corretto elemento 1 / elemento 2",
                value=3.5
            )

        with col2:
            nome1 = st.text_input("Nome elemento 1", "ferro")
            nome2 = st.text_input("Nome elemento 2", "ossigeno")

        if st.button("Verifica"):
            risultato = proust_verifica_composto(
                massa_elemento_1,
                massa_elemento_2,
                rapporto_corretto,
                nome1,
                nome2
            )

            st.markdown('<div class="result">', unsafe_allow_html=True)
            st.subheader("Risultato")
            st.write(risultato["risultato"])
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("Passaggi")
            for passo in risultato["passi"]:
                st.write(passo)


elif menu == "Legge di Dalton":
    st.header("🔢 Legge di Dalton")

    st.markdown("""
**La legge di Dalton dice:**

> Quando due elementi formano più composti, le masse di un elemento che si combinano
> con la stessa massa dell'altro stanno tra loro in rapporti semplici.
""")

    col1, col2 = st.columns(2)

    with col1:
        massa_a_primo = st.number_input(
            "Primo composto: massa elemento A, in grammi",
            value=5.5
        )

        massa_b_primo = st.number_input(
            "Primo composto: massa elemento B, in grammi",
            value=1.6
        )

        atomi_b_primo = st.number_input(
            "Atomi di B nel primo composto",
            min_value=1,
            value=1,
            step=1
        )

    with col2:
        rapporto_secondo = st.number_input(
            "Secondo composto: rapporto A/B",
            value=1.72
        )

        nome_a = st.text_input("Nome elemento A", "manganese")
        nome_b = st.text_input("Nome elemento B", "ossigeno")

    if st.button("Risolvi Dalton"):
        risultato = dalton_due_composti(
            massa_a_primo,
            massa_b_primo,
            rapporto_secondo,
            atomi_b_primo,
            nome_a,
            nome_b
        )

        st.markdown('<div class="result">', unsafe_allow_html=True)
        st.subheader("Risultato")
        st.write(risultato["risultato"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("Passaggi")
        for passo in risultato["passi"]:
            st.write(passo)


elif menu == "Massa molecolare":
    st.header("🧮 Massa molecolare")

    st.markdown("""
La massa molecolare si calcola sommando le masse atomiche di tutti gli atomi presenti nella formula.

Esempi:
- `H2O`
- `CO2`
- `H3PO4`
- `Ca(OH)2`
- `Mn3(PO4)2`
""")

    formula = st.text_input(
        "Inserisci la formula chimica",
        "H2O"
    )

    if st.button("Calcola massa molecolare"):
        try:
            risultato = calcola_massa_molecolare(formula)

            st.markdown('<div class="result">', unsafe_allow_html=True)
            st.subheader("Risultato")
            st.markdown(
                f"La massa molecolare di {formula_to_html(formula)} è {risultato['massa']}.",
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("Passaggi")
            for passo in risultato["passi"]:
                st.write(passo)

            st.subheader("Tabella di calcolo")
            st.dataframe(risultato["tabella"], use_container_width=True)

        except Exception as e:
            st.error(f"Errore: {e}")


