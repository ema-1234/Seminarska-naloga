import csv
from pathlib import Path

CSV_FILENAME = "nepremicnine_ljubljana.csv"

OSNOVNA_MAPA = Path.cwd()
path = OSNOVNA_MAPA / "SUROVI_PODATKI" / "nepremicnine_ljubljana.csv"

def nalozi_podatke(path):
    cene = []
    velikosti = []
    leta = []
    tipi = []

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            c_zapis = row["cena_€"]
            v_zapis = row["velikost_m2"]
            l_zapis = row["leto_izgradnje"]
            t_zapis = row["tip"]
            
            c_ocisceno = c_zapis.replace("€", "").replace(".", "").replace(",", ".").strip()
            v_ocisceno = v_zapis.replace(",", ".").strip()
            l_ocisceno = l_zapis.strip()
            t_ocisceno = t_zapis.strip()
            
            try:
                cena = float(c_ocisceno)
                velikost = float(v_ocisceno)
                leto = int(l_ocisceno)
                
                cene.append(cena)
                velikosti.append(velikost)
                leta.append(leto)
                tipi.append(t_ocisceno if t_ocisceno else None)

            except ValueError:
                continue
    return cene, tipi, velikosti, leta