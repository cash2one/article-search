# coding: utf-8


# exceptions
class InitError(Exception):
    pass

# importer base class
class DataImporter(object):
    """
        this function should return a formatted dict
    """
    def parse(self, *args, **kwargs):
        raise NotImplemented

    def __iter__(self):
        raise NotImplemented

