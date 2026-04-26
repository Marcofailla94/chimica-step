from openai import OpenAI
import streamlit as st


def get_openai_client():
    if "OPENAI_API_KEY" not in st.secrets:
        raise ValueError("Manca OPENAI_API_KEY nei Secrets di Streamlit")

    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


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

REGOLE:
- NON usare moli.
- NON usare numero di Avogadro.
- NON usare stechiometria avanzata.
- Usa linguaggio semplice.
- Spiega sempre passo passo.
- Alla fine scrivi sempre "Risultato finale".

FORMULE E CALCOLI:
Quando scrivi formule chimiche o calcoli numerici, usa SEMPRE questo formato:

[LATEX]2S + 3O_2 \\rightarrow 2SO_3[/LATEX]

Oppure:

[LATEX]x = 98 - 80 = 18\\,g[/LATEX]

Regole importanti:
- Non mettere formule chimiche fuori dai tag LATEX.
- Non andare a capo dentro i tag LATEX.
- Non scrivere parentesi quadre diverse.
- Usa sempre _ per i pedici, esempio O_2, SO_3, H_2O.
- Usa \\rightarrow per la freccia di reazione.
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


