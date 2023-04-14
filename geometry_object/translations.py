import csv

# Load translations
relation_translations = []
with open("geometry_object/relation_translations.csv", "r", encoding="utf-8") as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        relation_translations.append(row)
size = len(relation_translations)

type_translations = {"điểm" : "point", "đường_thẳng" : "line", "đoạn_thẳng" : "segment", "đoạn" : "segment", "đường_tròn" : "circle" , "tam_giác" : "triangle", "đa_giác" : "polygon",
                      "tia" : "ray", "tứ_giác" : "polygon"} 
assumptions = {1: "point", 2 : "segment", 3 : "triangle" , 4: "polygon", 5: "polygon", 6: "polygon"}