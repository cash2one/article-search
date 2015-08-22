# coding: utf-8

# parser base class
class DataParser(object):
    def parse(self, *args, **kwargs):
        raise NotImplemented


# importer base class
class DataImporter(object):
    # should set a parser class to parse data
    parser_class = DataParser

    class ParserClassError(Exception):
        pass

    def __init__(self):
        # check model class
        if not (self.parser_class and issubclass(self.parser_class, DataParser)):
            raise DataImporter.ParserClassError

    """
        iterate to get import data object
    """
    def data(self):
        raise NotImplemented

