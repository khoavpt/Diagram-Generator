from abc import ABC, abstractmethod

class GeometryObject(ABC):
    @abstractmethod
    def toGMBL(self):
        """
        Convert to GMBL command
        """
        pass

    @abstractmethod
    def summaries(self):
        """
        Return a summary string
        """
        pass

    @abstractmethod
    def printObject(self):
        """
        Print geometric objects to the terminal
        """
        pass