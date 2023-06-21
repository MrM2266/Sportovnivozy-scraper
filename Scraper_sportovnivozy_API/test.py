import json
import scraper

#filename = "models/bentley.json"
#
#file = open(filename, "r")
#data = json.load(file)
#file.close()
#
#dic = {}
#
#for key in data:
#    dic[data[key]] = key
#
#file = open("models/models.json", "a", encoding="utf-8")
#file.writelines(json.dumps(dic, indent=4))
#file.close()


#print(data["Aston Martin"])


print(scraper.ProcessPage("https://www.sportovnivozy.cz/novinky"))