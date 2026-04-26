from fractions import Fraction


def lavoisier_due_reagenti_un_prodotto(
    massa_reagente_noto,
    massa_prodotto,
    nome_reagente_noto,
    nome_reagente_incognito,
    nome_prodotto
):
    massa_incognita = massa_prodotto - massa_reagente_noto

    passi = [
        "1. Applico la legge di Lavoisier.",
        "La legge dice che la massa totale dei reagenti è uguale alla massa totale dei prodotti.",
        f"2. I reagenti sono {nome_reagente_noto} e {nome_reagente_incognito}.",
        f"3. Il prodotto è {nome_prodotto}.",
        f"4. Scrivo: massa {nome_reagente_noto} + massa {nome_reagente_incognito} = massa {nome_prodotto}.",
        f"5. Sostituisco i numeri: {massa_reagente_noto} + x = {massa_prodotto}.",
        f"6. Porto {massa_reagente_noto} dall'altra parte: x = {massa_prodotto} - {massa_reagente_noto}.",
        f"7. Risultato: x = {massa_incognita} g."
    ]

    return {
        "risultato": f"La massa di {nome_reagente_incognito} è {massa_incognita} g.",
        "passi": passi
    }


def lavoisier_due_reagenti_due_prodotti(
    massa_reagente_1,
    massa_reagente_2,
    massa_prodotto_noto,
    nome_reagente_1,
    nome_reagente_2,
    nome_prodotto_noto,
    nome_prodotto_incognito
):
    massa_totale_reagenti = massa_reagente_1 + massa_reagente_2
    massa_prodotto_incognito = massa_totale_reagenti - massa_prodotto_noto

    passi = [
        "1. Applico la legge di Lavoisier.",
        "La massa totale dei reagenti deve essere uguale alla massa totale dei prodotti.",
        f"2. Sommo le masse dei reagenti: {massa_reagente_1} + {massa_reagente_2} = {massa_totale_reagenti} g.",
        f"3. I prodotti sono {nome_prodotto_noto} e {nome_prodotto_incognito}.",
        f"4. Scrivo: massa prodotti = {massa_prodotto_noto} + x.",
        f"5. Quindi: {massa_prodotto_noto} + x = {massa_totale_reagenti}.",
        f"6. Ricavo x: x = {massa_totale_reagenti} - {massa_prodotto_noto}.",
        f"7. Risultato: x = {massa_prodotto_incognito} g."
    ]

    return {
        "risultato": f"La massa di {nome_prodotto_incognito} è {massa_prodotto_incognito} g.",
        "passi": passi
    }


def proust_trova_massa_secondo_elemento(
    massa_elemento_1,
    rapporto_elemento1_elemento2,
    nome_elemento_1,
    nome_elemento_2
):
    massa_elemento_2 = massa_elemento_1 / rapporto_elemento1_elemento2

    passi = [
        "1. Applico la legge di Proust.",
        "La legge dice che in un composto il rapporto tra le masse degli elementi è sempre costante.",
        f"2. Il rapporto dato è {nome_elemento_1}/{nome_elemento_2} = {rapporto_elemento1_elemento2}.",
        f"3. Questo significa: massa di {nome_elemento_1} / massa di {nome_elemento_2} = {rapporto_elemento1_elemento2}.",
        f"4. Sostituisco la massa nota: {massa_elemento_1} / x = {rapporto_elemento1_elemento2}.",
        f"5. Ricavo x: x = {massa_elemento_1} / {rapporto_elemento1_elemento2}.",
        f"6. Risultato: x = {massa_elemento_2:.2f} g."
    ]

    return {
        "risultato": f"La massa di {nome_elemento_2} è {massa_elemento_2:.2f} g.",
        "passi": passi
    }


def proust_verifica_composto(
    massa_elemento_1,
    massa_elemento_2,
    rapporto_corretto,
    nome_elemento_1,
    nome_elemento_2
):
    rapporto_osservato = massa_elemento_1 / massa_elemento_2

    differenza = abs(rapporto_osservato - rapporto_corretto)

    if differenza < 0.05:
        esito = "Sì, i dati rispettano la legge di Proust."
    else:
        esito = "No, i dati non rispettano il rapporto indicato."

    passi = [
        "1. Applico la legge di Proust.",
        f"2. Calcolo il rapporto tra le masse date: {nome_elemento_1}/{nome_elemento_2}.",
        f"3. Rapporto osservato = {massa_elemento_1} / {massa_elemento_2} = {rapporto_osservato:.2f}.",
        f"4. Rapporto corretto atteso = {rapporto_corretto}.",
        "5. Confronto i due rapporti.",
        f"6. Esito: {esito}"
    ]

    return {
        "risultato": esito,
        "passi": passi
    }


def dalton_due_composti(
    massa_a_primo,
    massa_b_primo,
    rapporto_a_b_secondo,
    atomi_b_primo,
    nome_a,
    nome_b
):
    rapporto_primo = massa_a_primo / massa_b_primo
    fattore = rapporto_primo / rapporto_a_b_secondo
    atomi_b_secondo = atomi_b_primo * fattore

    frazione = Fraction(atomi_b_secondo).limit_denominator(10)

    passi = [
        "1. Applico la legge di Dalton, detta anche legge delle proporzioni multiple.",
        "2. Questa legge si usa quando due elementi formano più composti diversi.",
        f"3. Nel primo composto calcolo il rapporto {nome_a}/{nome_b}.",
        f"{nome_a}/{nome_b} = {massa_a_primo} / {massa_b_primo} = {rapporto_primo:.2f}.",
        f"4. Nel secondo composto il rapporto {nome_a}/{nome_b} è {rapporto_a_b_secondo}.",
        "5. Confronto i due rapporti.",
        f"{rapporto_primo:.2f} / {rapporto_a_b_secondo} = {fattore:.2f}.",
        f"6. Il numero {fattore:.2f} indica come cambia la quantità di {nome_b}.",
        f"7. Se nel primo composto ci sono {atomi_b_primo} atomi di {nome_b}, nel secondo diventano:",
        f"{atomi_b_primo} × {fattore:.2f} = {atomi_b_secondo:.2f}."
    ]

    if frazione.denominator == 1:
        risultato = f"Nel secondo composto ci sono {frazione.numerator} atomi di {nome_b}."
        passi.append("8. Il risultato è già un numero intero.")
    else:
        risultato = (
            f"Il rapporto ottenuto equivale a {frazione.numerator} atomi di {nome_b} "
            f"ogni {frazione.denominator} unità di riferimento."
        )
        passi.append("8. Poiché non posso avere mezzi atomi, trasformo il risultato in un rapporto intero.")
        passi.append(f"9. {atomi_b_secondo:.2f} equivale circa a {frazione.numerator}/{frazione.denominator}.")

    return {
        "risultato": risultato,
        "passi": passi
    }
