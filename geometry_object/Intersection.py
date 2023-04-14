from geometry_object.GeometryObject import GeometryObject

class Intersection(GeometryObject):
    def __init__(self, name1, name2, intersect_name):
        self.name1 = name1
        self.name2 = name2
        self.intersect_name = intersect_name

    def toGMBL(self):
        """
        Convert to GMBL  define command
        """
        if self.name1.isupper():
            self.name1 = tuple(["line", self.name1[0], self.name1[1]])              
        if self.name2.isupper():
            self.name2 = tuple(["line", self.name2[0], self.name2[1]])
        gmbl = ["define", self.intersect_name, "point", ("inter-ll", self.name1, self.name2)]
        return tuple(gmbl)
    
    def summaries(self):
        summary = f"{self.intersect_name}(point): {self.name1}(line) cắt {self.name2}(line)\n"
        return summary
    
    def printObject(self):
        print(self.name1, self.name2, self.intersect_name)