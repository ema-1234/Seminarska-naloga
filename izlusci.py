import csv
import os
import re
from bs4 import BeautifulSoup

DIRECTORY = "C:/Users/emaom/OneDrive/Desktop/Seminarska naloga/SUROVI_PODATKI"
CSV_FILENAME = "nepremicnine_ljubljana.csv"


def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke kot niz."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        text = file_in.read()
    return text

def page_to_ads(page_content):
    """Funkcija poišče posamezne oglase s pomočjo BeautifulSoup in atributa itemprop='description'."""
    soup = BeautifulSoup(page_content, 'html.parser')

    descriptions = soup.find_all(attrs={"itemprop": "description"})
    blocks = []
    
    for desc in descriptions:

        parent = desc.find_parent('div')
        if parent:
            blocks.append(str(parent))
        else:
            blocks.append(str(desc))
            
    return blocks


def get_dict_from_ad_block(block):
  soup = BeautifulSoup(block, 'html.parser')

  desc_tag = soup.find(attrs={'itemprop': 'description'})
  opis = desc_tag.get_text(strip=True) if desc_tag else ''

  cena = 'Ni podatka'
  h6_tag = soup.find('h6')
  if h6_tag:
    cena = h6_tag.get_text(strip=True)
  else:
    meta_tag = soup.find(attrs={'itemprop': 'price'})
    if meta_tag:
      cena = meta_tag.get('content')
    else:
      cena_match = re.search(r'Cena:\s*([\d\.,]+)', opis, re.IGNORECASE)
      if cena_match:
        cena = cena_match.group(1)

  if cena and cena != 'Ni podatka':
    prva_cena_match = re.search(r'([\d\.]+[\d,]*)', cena)
    if prva_cena_match:
      cena = prva_cena_match.group(1)

  if not opis and cena == 'Ni podatka':
    return None

  velikost_match = re.search(r'(\d+[\d,\.]*)\s*m2', opis, re.IGNORECASE)
  velikost = velikost_match.group(1) if velikost_match else None

  leto_match = re.search(
      r'(?:zgrajeno|gradnje|l\.)\s*[\.,]?\s*(\d{4})', opis, re.IGNORECASE
  )
  leto_izgradnje = leto_match.group(1) if leto_match else None

  tip_match = re.search(
      r'(\d+(?:\s+in\s+več)?-sobno|garsonjera|penthouse)', opis, re.IGNORECASE
  )
  tip = tip_match.group(1) if tip_match else None

  return {
      'velikost_m2': velikost,
      'leto_izgradnje': leto_izgradnje,
      'tip': tip,
      'cena_€': cena,
  }

def ads_from_file(filename, directory):
    """Prebere datoteko in jo pretvori v seznam slovarjev oglasov."""
    page_content = read_file_to_string(directory, filename)
    blocks = page_to_ads(page_content)
    ads = [get_dict_from_ad_block(block) for block in blocks]
    return [ad for ad in ads if ad is not None]


def write_csv(fieldnames, rows, directory, filename):
    """Zapiše vrednosti v CSV datoteko."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8', newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_ads_to_csv(ads, directory, filename):
    """Preveri podatke in jih zapiše v CSV datoteko."""
    if not ads:
        print("Seznam oglasov je prazen, ničesar ni za zapisati v CSV.")
        return
        
    assert ads and all(j.keys() == ads[0].keys() for j in ads)
    fieldnames = list(ads[0].keys())
    write_csv(fieldnames, ads, directory, filename)


if __name__ == '__main__':
    print("Berem HTML datoteke in izluščujem oglase...")
    vsi_oglasi = []
    
    for i in range(1, 31):
        filename = f"nepremicnine_stran_{i}.html"
        try:
            ads = ads_from_file(filename, DIRECTORY)
            vsi_oglasi.extend(ads)
        except FileNotFoundError:
            pass

    print(f"Najdenih in obdelanih veljavnih oglasov: {len(vsi_oglasi)}")
    
    write_ads_to_csv(vsi_oglasi, DIRECTORY, CSV_FILENAME)
    print(f"Podatki so uspešno shranjeni v {CSV_FILENAME}")