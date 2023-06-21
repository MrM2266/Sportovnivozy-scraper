# Sportovnivozy.cz scraper
- součástí aplikace jsou dvě komponenty - scraper, který poskytuje data pomocí API + script, který porovnává zadané auto s online nabídkou
- soubor find_similar_car obsahuje script, který porovná auto definované v souboru find_similar_car\neznam_cenu.json s nabídkou podobného modelu na serveru sportovnivozy.cz
- jsou podporovány pouze značky a modely uvedené v Scraper_sportovnivozy_API\codes\brand_code.json a Scraper_sportovnivozy_API\codes\models.json
- script vyžaduje běžící scraper API na url zadané v find_similar_car\conf.json
- na API posílá dotaz na scraping modelu zadaného v find_similar_car\neznam_cenu.json a dostává výsledky strukturovné v json
- provede vyhodnocení a zobrazí auto nejvíce podobné zadanému autu - vyhodnocuje na základě najetých kilometrů, objemu motoru, výkonu motoru a roku výroby
