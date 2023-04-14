import csv

from geometry_object.GeometryObject import GeometryObject
from geometry_object.translations import relation_translations, type_translations, assumptions, size

class BasicGeometryObject(GeometryObject):
    def __init__(self, geometry_type1, name1, relation, geometry_type2, name2):
        self.geometry_type1 = geometry_type1
        self.name1 = name1
        self.relation = relation
        self.geometry_type2 = geometry_type2
        self.name2 = name2

    def process(self, memories):
        """
        If geometry type is not mentioned, look in memories or make assumptions.
        """
        self.geometry_type1, self.name1 = preprocess(self.geometry_type1, self.name1, memories)
        if self.relation != "none":
            self.geometry_type2, self.name2 = preprocess(self.geometry_type2, self.name2, memories)

    def toGMBL(self):
        """
        Convert to GMBL param or define command.
        param commands: (param <string> <type> <optional-parameterization>) or (param (<string>, ..., <string>) <parameterization>)
        define commands: (define <string> <type> <value>)
        """
        if len(self.name1) > 1 and self.name1.isupper():
            self.name1 = tuple(letter for letter in self.name1)

        gmbl = [self.name1, self.geometry_type1]
        if self.relation == "none":
            gmbl.insert(0, "param")
        else:
            for i in range(size):
                if self.name2.isupper():
                    if len(self.name2) != 2 or self.geometry_type2 != "line":
                        parameterization = [letter for letter in self.name2]
                    else:
                        parameterization = [tuple(["line", self.name2[0], self.name2[1]])]
                else:
                    parameterization = [self.name2]
                if self.relation == relation_translations[i]["vietnamese"]:
                    if (self.geometry_type2 == relation_translations[i]["geometric_type2"] or relation_translations[i]["geometric_type2"] == "") and (self.geometry_type1 == relation_translations[i]["geometric_type1"] or relation_translations[i]["geometric_type1"] == ""):
                        parameterization.insert(0, relation_translations[i]["gmbl"])
                        gmbl.insert(0, relation_translations[i]["command"])
                        gmbl.append(tuple(parameterization))
        return tuple(gmbl)

    def toGMBLassert(self):
        """
        Convert to GMBL assert command: (assert <predicate>)
        """
        gmblCondition = ["assert"]
        predicate = []
        for i in range(size):
            if self.relation == relation_translations[i]["vietnamese"]:
                if (self.geometry_type2 == relation_translations[i]["geometric_type2"] or relation_translations[i]["geometric_type2"] == "") and (self.geometry_type1 == relation_translations[i]["geometric_type1"] or relation_translations[i]["geometric_type1"] == ""):
                    predicate.append(relation_translations[i]["gmbl"])

        for name, type in [(self.name1, self.geometry_type1), (self.name2, self.geometry_type2)]:
            if name.isupper():
                if len(name) != 2 or type!= "line":
                    predicate += [letter for letter in name]
                else:
                    predicate += [tuple(["line", name[0], name[1]])]
            else:
                predicate += [name]


        gmblCondition.append(tuple(predicate))
        return tuple(gmblCondition)

    def summaries(self):
        summary = f"{self.name1}({self.geometry_type1})"
        if self.relation != "none":
            summary += f": {self.relation} {self.name2}({self.geometry_type2})\n"
        return summary
    
    def printObject(self):
        """
        Print geometric objects to the terminal
        """
        print(self.geometry_type1, self.name1, self.relation, self.geometry_type2, self.name2)
        

def preprocess(type, name, memories):
    # If  this geometry type is not mentioned in this sentence, check if it was mentioned before
    if type == "none":
        for object_type, object_name in memories:
            if name == object_name:
                type = type_translations[object_type.lower()]
        if type == "none" and name.isupper():
            # If geometry type is still none, makes assumptions base on the length of the name
            type = assumptions[len(name)]
    else:
        type = type_translations[type.lower()]
    return type, name