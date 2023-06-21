from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import scraper
import json

def LoadJson(filename):
    file = open(filename, "r")
    data = json.load(file)
    file.close()
    return data

def GetLinkModel(brand, model):
    link = "https://www.sportovnivozy.cz/model-"
    link += brands[brand] + "-" + models[brand][model] + "-" + brand + "-" + model
    return link

def GetLinkZnacka(brand):
    link = "https://www.sportovnivozy.cz/znacka-"
    link += brands[brand] + "-" + brand
    print(link)
    return link


brands = LoadJson("codes/brand_code.json")
models = LoadJson("codes/models.json")
app = FastAPI()

@app.get("/main_page")
async def get_main_page():
    try:
        print("main")
        page_data = scraper.ProcessPage("https://www.sportovnivozy.cz")
    except:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(content = page_data)

@app.get("/latest")
async def get_latest():
    print("latest")
    try:
        page_data = scraper.ProcessPage("https://www.sportovnivozy.cz/novinky")
    except:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(content = page_data)

@app.get("/get_page")
async def get_main_page(link: str):
    print("get_page")
    try:
        page_data = scraper.ProcessPage(link)
    except:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(content = page_data)

@app.get("/{brand}/{model}")
async def get_car(brand: str, model: str):
    print("brand, model")
    try:
        page_data = scraper.ProcessPage(GetLinkModel(brand, model))
    except:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(content = page_data)

@app.get("/{brand}")
async def get_brand(brand: str):
    print("brand")
    try:
        page_data = scraper.ProcessPage(GetLinkZnacka(brand))
    except:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(content = page_data)

