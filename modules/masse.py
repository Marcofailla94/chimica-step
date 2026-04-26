import pandas as pd

from modules.bilanciamento import parse_formula


MASSE_ATOMICHE = {
    "H": 1.008,
    "C": 12.01,
    "N": 14.01,
    "O": 16.00,
    "Na": 22.99,
    "Mg": 24.31,
    "Al": 26.98,
    "Si": 28.09,
    "P": 30.97,
    "S": 32.06,
    "Cl": 35.45,
    "K": 39.10,
    "Ca": 40.08,
    "Mn": 54.94,
    "Fe": 55.85,
    "Cu": 63.55,
    "Zn": 65.38,
    "Ag": 107.87,
    "I": 126.90,
    "Ba": 137.33,
}


def calcola_massa_molecolare(formula):
    composizione = parse_formula(formula)

    totale = 0
    righe = []
    passi = []

    passi.append("1. Leggo la formula chimica.")
    passi.append("2. Individuo gli elementi presenti.")
    passi.append("3. Per ogni elemento moltiplico la massa atomica per il numero di atomi.")
    passi.append("4. Sommo tutti i risultati.")

    for elemento, numero_atomi in composizione.items():
        if elemento not in MASSE_ATOMICHE:
            raise ValueError(f"L'elemento {elemento} non è presente nella tabella interna.")

        massa_atomica = MASSE_ATOMICHE[elemento]
        contributo = massa_atomica * numero_atomi
        totale += contributo

        righe.append({
            "Elemento": elemento,
            "Numero atomi": numero_atomi,
            "Massa atomica": massa_atomica,
            "Calcolo": f"{massa_atomica} × {numero_atomi}",
            "Contributo": round(contributo, 2)
        })

        passi.append(
            f"{elemento}: {massa_atomica} × {numero_atomi} = {contributo:.2f}"
        )

    passi.append(f"Massa molecolare totale = {totale:.2f}.")

    return {
        "massa": round(totale, 2),
        "tabella": pd.DataFrame(righe),
        "passi": passi
    }
