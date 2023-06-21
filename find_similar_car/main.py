import json
import requests

def LoadJson(filename):
    try:
        file = open(filename, "r")
        data = json.load(file)
        file.close()
        return data
    except:
        raise SystemExit(f"Nepodarilo se nacit json {filename}")
    
def LoadConfig():
    try:
        return LoadJson("conf.json")
    except:
        print("Nepodarilo se nacist soubor konfigurace. Pouzivam defaultni hodnoty.")
        return {"scraper_api_url":"http://localhost:6060"}

def compute_parameter_match(from_dataset, from_input):
    if (from_dataset != None) and (from_input != None):
        try:
            return (1 - abs(float(from_dataset) - float(from_input)) / float(from_input))
        except:
            return 0.5
    else:
        return 0.5
    
def find_best_match(car_to_match, dataset):
    output = {"match":0, "index":None}

    for car in dataset:
        objem_match = compute_parameter_match(car["objem"], car_to_match["objem"])
        rok_match = compute_parameter_match(car["rok"], car_to_match["rok"])
        najezd_match = compute_parameter_match(car["najezd"], car_to_match["najezd"])
        vykon_match = compute_parameter_match(car["vykon"], car_to_match["vykon"])

        total_match = (objem_match + rok_match + najezd_match + vykon_match) / 4
        if (total_match > output["match"]):
            output["match"] = total_match
            output["index"] = dataset.index(car)

    return output

def obtain_data(brand, model, api_url):
    url = api_url + "/" + brand + "/" + model
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise SystemExit("API vraci chybovy kod")
        data = json.loads(response.text)
        return data
    except:
        raise SystemExit("Nepodařilo se nacist data z API")
    
def show_raw_car_data(out, data):
    print("Raw data")
    print("=" * 100)
    print(out)
    print(data[int(out["index"])])

def show_formarted_car_data(out, data):
    print("Formated data")
    print("=" * 100)
    print(f"Shoda:  {out['match']}\nNazev:  {data[int(out['index'])]['nazev']}")
    print(f"Rok:    {data[int(out['index'])]['rok']}")
    print(f"Najezd: {data[int(out['index'])]['najezd']} km")
    print(f"Objem:  {data[int(out['index'])]['objem']} cm3")
    print(f"Vykon:  {data[int(out['index'])]['vykon']} kW")
    print(f"Cena:   {data[int(out['index'])]['cena']} kč")
    print(f"Link:   {data[int(out['index'])]['link']}")


conf = LoadConfig()
my_car = LoadJson("neznam_cenu.json")
data = obtain_data(my_car["znacka"], my_car["model"], conf["scraper_api_url"])
out = find_best_match(my_car, data)

show_formarted_car_data(out, data)