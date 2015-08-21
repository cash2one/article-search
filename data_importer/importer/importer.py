# coding: utf-8

import os
import re
import sys
import traceback
import hashlib
import inspect
import copy_reg
import types
import random
from functools import partial
from multiprocessing import Pool


# exceptions
class InitError(Exception):
    pass
class MethodNotImplemented(Exception):
    pass


# importer base class
class DataImporter(object):
    """
        this function should return a formatted dict
    """
    def parse(self, *args, **kwargs):
        raise MethodNotImplemented

    def __iter__(self):
        raise MethodNotImplemented

