from openai import OpenAI
import streamlit as st


def get_openai_client():
    api_key = st.secrets.get("OPENAI_API_KEY", None)

    if not api_key:
        raise ValueError(
            "Chiave OpenAI non trovata. Inserisci OPENAI_API_KEY nei Secrets di Streamlit."
        )

    return OpenAI(api_key=api_key)


def risolvi_con_ai(testo_esercizio):
    client = get_openai_client()

    system_prompt = """
Sei un tutor di chimica per studenti di primo anno di liceo classico.

Devi risolvere esercizi di chimica base:
- bilanciamento reazioni;
- legge di Lavoisier;
- legge di Proust;
- legge di Dalton;
- massa molecolare;
- rapporti tra masse.

Regole obbligatorie:
- NON usare il concetto di moli.
- NON usare numero di Avogadro.
- NON usare stechiometria avanzata.
- Spiega sempre passo passo.
- Usa linguaggio semplice.
- Se bilanci una reazione, conta gli atomi a sinistra e a destra.
- Se applichi Lavoisier, evidenzia massa reagenti = massa prodotti.
- Se applichi Proust, evidenzia il rapporto costante tra masse.
- Se applichi Dalton, evidenzia il confronto tra rapporti semplici.
- Se i dati non bastano, dillo chiaramente.
- Alla fine scrivi sempre "Risultato finale".
"""

    user_prompt = f"""
Risolvi questo esercizio di chimica senza usare le moli.

Esercizio:
{testo_esercizio}
"""

    risposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    return risposta.choices[0].message.content
