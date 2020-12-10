import sys
from importlib import import_module
  
# dynamic import  
def dynamic_import(name): 

    return import_module(name)
