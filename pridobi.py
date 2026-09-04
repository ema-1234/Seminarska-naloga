import random
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje"
SHRANJEVALNA_MAPA = Path("C:/Users/emaom/OneDrive/Desktop/Seminarska naloga/SUROVI_PODATKI")


def prenesi_z_brskalnikom(skupno_strani: int = 1):
    SHRANJEVALNA_MAPA.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome", 
            headless=False, 
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context()
    # #with sync_playwright() as p:
    #     browser = p.chromium.launch(channel="chrome", headless=True)
    #     context = browser.new_context(
    #         user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    #         locale="sl-SI",
    #     )
    
        page = context.new_page()

        for st_strani in range(1, skupno_strani + 1):
            url = f"{BASE_URL}/{st_strani}/" if st_strani > 1 else f"{BASE_URL}/"

            try:
                response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
                
                if response and response.status == 200:
                    time.sleep(random.uniform(2.5, 4.0))
                    html_vsebina = page.content()

                    datoteka = SHRANJEVALNA_MAPA / f"nepremicnine_stran_{st_strani}.html"
                    datoteka.write_text(html_vsebina, encoding="utf-8")
                    
                    print(f"[OK] Uspešno shranjena stran {st_strani}")
                else:
                    status = response.status if response else "Brez odziva"
                    print(f"[NAPAKA] Stran {st_strani} vrnila status: {status}")

            except Exception as e:
                print(f"[NAPAKA] Pri prenosu strani {st_strani}: {e}")

        browser.close()


if __name__ == "__main__":
    prenesi_z_brskalnikom(skupno_strani=30)


