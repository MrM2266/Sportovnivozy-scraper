import datetime
import re
import requests
from bs4 import BeautifulSoup


def GetPage(URL):
    #vrací html stránku na zadané adrese jako text - respektive vrací odpověď na get jako text
    try:
        page = requests.get(URL)
        page.encoding = "utf-8"
        return page.text #zde si z request objectu dostaneme odpověd na náš get (=stránka html) získáme text odpovědi jako string s utf-8
    except:
        raise SystemExit("Nepodařilo se získat zadanou URL")

def GetCuttedPage(page, oddelovac):
    #odstaraní ze stránky nepotřebný začátek a konec html kódu
    try:
        first = re.search(oddelovac, page) #usekne přední nepotřebnou část html
        last = re.search("<div id=.bottom.>", page) #usekne zadní nepotřebnou část html
        return page[first.end():last.start()]
    except:
        raise SystemExit("Nepodařilo se naparsovat (oseknout) stránku")

def GetCarsHTML(cutted_page, oddelovac):
    #rozdělí stránku na html kód jednotlivých aut - vrací pole, kde každý prvek je html kód pro jedno auto
    try:
        return re.split(oddelovac, cutted_page) #každá položka listu obsahuje kód jednoho auta
    except:
        raise SystemExit("Nepodarilo se naparsovat jednotliva auta")

def WriteCarsToFiles(cars):
    #pouze pro ladění - zapíše html kód aut do souborů - každé auto do svého
    for i in range(0, len(cars)):
        file = open(f"cars{i}.html", "w", encoding="utf-8")
        file.writelines(cars[i])
        file.close()

def GetPrice(price):
    #snaží se z html kódu auta naparsovat cenu a vrátit ji
    try:
        price = price.replace("\n", "")
        price = re.sub("\s{1,}", "", price)
        price = re.search("[0-9]+", price).group()
        return price
    except:
        return None

def GetDescription(desc):
    #odstraní z popisu všechny nechtěné znaky včetně mezer
    try:
        desc = desc.replace("\n", "")
        desc = re.sub("\s{1,}", "", desc)
        return desc
    except:
        return None

def GetName(name):
    #odstraní z názvu auta všechny nechtěné znaky včetně mezer
    try:
        name = name.replace("\n", "")
        name = re.sub("\s{2,}", " ", name)
        return name[:-1]
    except:
        return None

def GetYear(desc):
    #snaží se v popisu aut najít rok výroby
    try:
        match = re.search("[0-9]{4}\/", desc)
        return desc[match.start():match.end()-1]
    except:
        return None

def GetMileage(desc):
    #snaží se v popisu aut najít nájezd
    try:
        match = re.search("[0-9]{1,}Km", desc)
        return desc[match.start():match.end()-2]
    except:
        return None

def GetEngineSize(desc):
    #snaží se v popisu aut najít objem motoru
    try:
        match = re.search("[0-9]{1,}ccm", desc)
        return desc[match.start():match.end()-3]
    except:
        return None

def GetPower(desc):
    #snaží se v popisu aut najít výkon
    try:
        match = re.search("[0-9]{1,}kW", desc)
        return desc[match.start():match.end()-2]
    except:
        return None

def GetLink(code, url_prefix):
    try:
        match = re.search("<a href=.*? ", code)
        out = code[match.start()+9:match.end()-2]
        out = url_prefix + out
        return out
    except:
        return None

def GetURLPrefix(URL):
    #vrací ze zadané url adresy pouze název do prvního /
    #prefix je použit pro tvorbu linků ve fci GetLink
    try:
        match = re.search("https://.*?/", URL)
        return URL[match.start():match.end()]
    except:
        return ""


def GetSortedData(cars, URL):
    #vrací pole, kde každý prvek je dict obsahující informace o jednom autě
    #vstupní parametr cars je pole, kde každý prvek obsahuje html kód jednoho auta - z něj se zde dostanou všechny informace a upraví se
    data = []

    for car in cars:
        try:
            temp = BeautifulSoup(car, "html.parser")
            vt_class = temp.find_all(class_="vt")
            t120pc_class = temp.find(class_="T120pc")

            nazev = GetName(vt_class[0].getText())
            popis = GetDescription(vt_class[1].getText())
            link = GetLink(str(vt_class[0]), GetURLPrefix(URL))
            cena = GetPrice(t120pc_class.getText())

            car_data = {
                "nazev": nazev,
                "rok": GetYear(popis),
                "najezd":GetMileage(popis),
                "objem":GetEngineSize(popis),
                "vykon":GetPower(popis),
                "cena":cena,
                "link":link}

            data.append(car_data)

        except:
            print("Chyba na jednom z bloku dat v poli cars")
            continue

    return data

def WriteJson(json_data, name = "data_"):
    #zapisuje data do json s kódováním utf-8
    now = datetime.datetime.now()
    filename = name + now.strftime("%d_%m_%Y_%H%M") + ".json"
    file = open(filename, "w", encoding="utf-8")
    file.writelines(json_data)
    file.close()

def ProcessPage(URL):
    #zpracuje jednu zadanou stránku - stáhne si jí, odstraní nepotřebný kód, rozdělí ji na html kód jednotlivých aut
    #z html kódu pro jednotlivá auta se dostanou informace a ty se uloží do json

    oddelovac = "<table class=.vypisDilo W100pc T100pc.*>" #oddeluje jednotliva auta od sebe

    page_text = GetCuttedPage(GetPage(URL), oddelovac) #stáhne stránku a rovnou z ní odstraní nepotřebný začátek a konec
    cars_html = GetCarsHTML(page_text, oddelovac) #rozdělí html kód na kód pro jednotlivá auta
    page_data = GetSortedData(cars_html, URL)#vytvoří json - nechá naparsovat data a ta rovnou pošle do json.dumps
    #WriteJson(json_data, file_prefix) #provede zápis do souboru; file_prefix udává, co se má zapsat do názvu souboru před datum a čas
    return page_data