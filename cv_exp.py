import json

with open('documents/CV/cv.json', 'r', encoding="utf-8") as file:
    data_cv = json.load(file)

with open('static/info_json/experience.json', 'r', encoding="utf-8") as file:
    data_xp = json.load(file)

class CvXp:
    def getCV(lang="esp"):
        try:
            return data_cv[lang]
        except:
            return []

    def getXp(lang = "esp"):
        try:
            return data_xp[lang]
        except:
            return []
