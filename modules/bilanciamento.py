import re
import math
from collections import defaultdict

import pandas as pd
import sympy as sp


def formula_to_html(formula: str) -> str:
    return re.sub(r'(\d+)', r'<sub>\1</sub>', formula)


def parse_formula(formula: str):
    formula = formula.strip()
    tokens = re.findall(r'([A-Z][a-z]?|\(|\)|\d+)', formula)

    stack = [defaultdict(int)]
    i = 0

    while i < len(tokens):
        tok = tokens[i]

        if tok == '(':
            stack.append(defaultdict(int))
            i += 1

        elif tok == ')':
            group = stack.pop()
            i += 1

            moltiplicatore = 1
            if i < len(tokens) and tokens[i].isdigit():
                moltiplicatore = int(tokens[i])
                i += 1

            for elemento, numero in group.items():
                stack[-1][elemento] += numero * moltiplicatore

        elif re.match(r'[A-Z][a-z]?$', tok):
            elemento = tok
            i += 1

            numero = 1
            if i < len(tokens) and tokens[i].isdigit():
                numero = int(tokens[i])
                i += 1

            stack[-1][elemento] += numero

        else:
            raise ValueError("Formula non valida.")

    if len(stack) != 1:
        raise ValueError("Parentesi non bilanciate.")

    return dict(stack[0])


def split_reaction(reaction: str):
    reaction = reaction.replace("→", "->").replace("=", "->")

    if "->" not in reaction:
        raise ValueError("Usa la freccia -> tra reagenti e prodotti.")

    sinistra, destra = reaction.split("->", 1)

    reagenti = [x.strip() for x in sinistra.split("+") if x.strip()]
    prodotti = [x.strip() for x in destra.split("+") if x.strip()]

    return reagenti, prodotti


def mcm_lista(numeri):
    risultato = 1

    for n in numeri:
        risultato = abs(risultato * n) // math.gcd(risultato, n)

    return risultato


def bilancia_reazione(reaction: str):
    reagenti, prodotti = split_reaction(reaction)

    formule = reagenti + prodotti
    formule_analizzate = [parse_formula(f) for f in formule]

    elementi = sorted(set().union(*[set(f.keys()) for f in formule_analizzate]))

    matrice = []

    for elemento in elementi:
        riga = []

        for i, formula in enumerate(formule_analizzate):
            numero = formula.get(elemento, 0)

            if i >= len(reagenti):
                numero *= -1

            riga.append(numero)

        matrice.append(riga)

    M = sp.Matrix(matrice)
    soluzioni = M.nullspace()

    if not soluzioni:
        raise ValueError("Non riesco a bilanciare questa reazione.")

    vettore = soluzioni[0]

    denominatori = [x.q for x in vettore]
    mcm = mcm_lista(denominatori)

    coefficienti = [int(x * mcm) for x in vettore]

    if any(c < 0 for c in coefficienti):
        coefficienti = [-c for c in coefficienti]

    divisore = abs(coefficienti[0])

    for c in coefficienti[1:]:
        divisore = math.gcd(divisore, abs(c))

    coefficienti = [c // divisore for c in coefficienti]

    parti_sinistra = []
    parti_destra = []

    for i, formula in enumerate(reagenti):
        coeff = coefficienti[i]
        testo = formula_to_html(formula)

        if coeff != 1:
            testo = str(coeff) + " " + testo

        parti_sinistra.append(testo)

    for j, formula in enumerate(prodotti):
        coeff = coefficienti[len(reagenti) + j]
        testo = formula_to_html(formula)

        if coeff != 1:
            testo = str(coeff) + " " + testo

        parti_destra.append(testo)

    equazione_html = " + ".join(parti_sinistra) + " → " + " + ".join(parti_destra)

    passi = []

    passi.append("1. Divido la reazione in reagenti e prodotti.")
    passi.append(f"Reagenti: {', '.join(reagenti)}")
    passi.append(f"Prodotti: {', '.join(prodotti)}")

    passi.append("2. Conto gli atomi presenti in ogni formula.")
    for formula, conteggio in zip(formule, formule_analizzate):
        dettagli = ", ".join([f"{el}: {num}" for el, num in conteggio.items()])
        passi.append(f"{formula} contiene {dettagli}.")

    passi.append("3. Inserisco dei coefficienti davanti alle formule.")
    passi.append("4. Non modifico mai i numeri piccoli dentro le formule.")
    passi.append("5. Controllo che ogni elemento abbia lo stesso numero di atomi a sinistra e a destra.")

    controllo = []

    for elemento in elementi:
        atomi_sinistra = 0
        atomi_destra = 0

        for i, formula in enumerate(formule_analizzate):
            if i < len(reagenti):
                atomi_sinistra += coefficienti[i] * formula.get(elemento, 0)
            else:
                atomi_destra += coefficienti[i] * formula.get(elemento, 0)

        controllo.append({
            "Elemento": elemento,
            "Atomi nei reagenti": atomi_sinistra,
            "Atomi nei prodotti": atomi_destra,
            "Bilanciato": "Sì" if atomi_sinistra == atomi_destra else "No"
        })

    return {
        "equazione_html": equazione_html,
        "passi": passi,
        "tabella": pd.DataFrame(controllo)
    }
