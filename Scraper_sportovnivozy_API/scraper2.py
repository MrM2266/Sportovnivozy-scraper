import requests
from bs4 import BeautifulSoup
import datetime
import json

payload = {}
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
  'Accept': '*/*',
  'Accept-Language': 'cs,sk;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept-Encoding': 'gzip, deflate, br',
  'X-Requested-With': 'XMLHttpRequest',
  'Connection': 'keep-alive',
  'Referer': 'https://www.autoesa.cz/vsechna-auta?zobrazeni=2',
  #'Cookie': 'PHPSESSID=6kftq3uhi6qno1lrsi6foh5svp; firstPage=www.autoesa.cz^%^2Fvsechna-auta; source=google-ads; beforeUrl=https^%^3A^%^2F^%^2Fwww.autoesa.cz^%^2Fvsechna-auta^%^3Fzobrazeni^%^3D2; _ga=GA1.2.1756478363.1685575738; cconsent={version:1,categories:{necessary:{wanted:true},analytics:{wanted:true},marketing:{wanted:true}},services:^[configcookies,ganalytics,smartsupp,fbpixel,googleads,sklik,exponea,adform,progsol,rtbhouse^]}; _ga_T4XBBMXQM7=GS1.1.1687741149.3.1.1687743144.15.0.0; _ga=GA1.3.1756478363.1685575738; _fbc=fb.1.1685575769843.IwAR059zxQ4U3bTFm7hvMk0X_enW2e_09ZcJn6w2E7SWGH_7g4V9wzee5RvYs; _fbp=fb.1.1685575740165.427303706; lastUrl=https^%^3A^%^2F^%^2Fwww.autoesa.cz^%^2Fvsechna-auta^%^3Fzobrazeni^%^3D2^%^26stranka^%^3D1; _gcl_au=1.1.544933612.1685575770; __exponea_etc__=4b51b1d0-0dd5-4e92-8e11-fdd8a34639b2; hp-banner=1; SERVERID=www5^|ZJjqn^|ZJjjL; __exponea_time2__=-1.4599831104278564; _gid=GA1.2.650424759.1687736162; _gid=GA1.3.650424759.1687736162; _ga_HLJ8T44W5M=GS1.3.1687741228.2.1.1687743143.0.0.0; url=https^%^3A^%^2F^%^2Fwww.autoesa.cz^%^2Fvsechna-auta^%^3Fzobrazeni^%^3D2; ppc=Google+Ads; _gcl_aw=GCL.1687736857.Cj0KCQjwy9-kBhCHARIsAHpBjHi7DMnQqxUmnV_l_0ZmsxrFpCo2Idj73vdDEwA4j2QrMNVsz4PQtJkaAqPmEALw_wcB; _gac_UA-4745099-1=1.1687736858.Cj0KCQjwy9-kBhCHARIsAHpBjHi7DMnQqxUmnV_l_0ZmsxrFpCo2Idj73vdDEwA4j2QrMNVsz4PQtJkaAqPmEALw_wcB; _gac_UA-4745099-23=1.1687736858.Cj0KCQjwy9-kBhCHARIsAHpBjHi7DMnQqxUmnV_l_0ZmsxrFpCo2Idj73vdDEwA4j2QrMNVsz4PQtJkaAqPmEALw_wcB; _dc_gtm_UA-4745099-1=1; _dc_gtm_UA-4745099-23=1; _uetsid=0b462e6013b111ee8aa3494701528985; _uetvid=eacf5210000a11eea104d1bc6649d6c7; PHPSESSID=r8su6vvrc00lf4rs5kte7b467t; SERVERID=www8|ZJjq1|ZJjq1; beforeUrl=https%3A%2F%2Fwww.autoesa.cz%2Fvsechna-auta%3Fzobrazeni%3D2%26stranka%3D2; lastUrl=https%5E%25%5E3A%5E%25%5E2F%5E%25%5E2Fwww.autoesa.cz%5E%25%5E2Fvsechna-auta%5E%25%5E3Fzobrazeni%5E%25%5E3D2; url=https%3A%2F%2Fwww.autoesa.cz%2Fvsechna-auta%3Fzobrazeni%3D2%26stranka%3D2',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin'
}

def html(lastPage):
    elements=[]
    for i in range(1, lastPage):
        url = f"https://www.autoesa.cz/vsechna-auta?zobrazeni=2&stranka={i}"
        response = requests.request("GET", url, headers=headers, data=payload)
        modified=response.text.replace("\\n", "").replace("\\", "").replace("&nbsp;","")
        soup = BeautifulSoup(modified,'html.parser')
        elements.append(soup.find_all('div', class_="car_item__inner"))
    return elements

def WriteJson(json_data, name = "data_"):
    now = datetime.datetime.now()
    filename = name + now.strftime("%d_%m_%Y_%H%M") + ".json"
    file = open(filename, "w", encoding="utf-8")
    file.writelines(json_data)
    file.close()

def GetCars(cars):
    data=[]
    for element in cars:
        for item in element:    
            span_element_title = item.find('span', class_='car-title')
            if span_element_title:
                span_text_title = span_element_title.get_text(strip=True)
            
            div_element_year = item.find('div', class_='car_item__icon icon_year')
            if div_element_year:
                div_text_year = div_element_year.get_text(strip=True)

            div_element_power = item.find('div', class_='car_item__icon icon_power')
            if div_element_power:
                div_text_power = div_element_power.get_text(strip=True)

            div_element_fuel = item.find('div', class_='car_item__icon icon_fuel')
            if div_element_fuel:
                div_text_fuel = div_element_fuel.get_text(strip=True)

            div_element_range = item.find('div', class_='car_item__icon icon_range')
            if div_element_range:
                div_text_range = div_element_range.get_text(strip=True)

            span_element_price = item.find_all('span', class_='price')
            second_span_price=span_element_price[1]
            span_text_price=second_span_price.get_text(strip=True)

            match_data = {
                "nazev": span_text_title,
                "rok": div_text_year,
                "najezd": div_text_range,
                "vykon": div_text_power,
                "palivo": div_text_fuel,
                "cena": span_text_price 
                }
            data.append(match_data)
    return data

def GetLastPage():
    url = f"https://www.autoesa.cz/vsechna-auta?zobrazeni=2&stranka=1"
    response = requests.request("GET", url, headers=headers, data=payload)
    modified=response.text.replace("\\n", "").replace("\\", "").replace("&nbsp;","")
    soup = BeautifulSoup(modified,'html.parser')

    number=soup.find("li", class_="dots dots-last").get_text(strip=True).replace("... ","")
    return int(number)

def ProcessPage(file_prefix = "data_"):
    lastPage=GetLastPage()
    cars=html(lastPage)
    print(cars)
    dataAut=GetCars(cars)
    json_data = json.dumps(dataAut, indent=4, ensure_ascii=False)
    WriteJson(json_data, file_prefix)

ProcessPage(file_prefix=r"autoesa_")            


