import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "tOSM - Tiny Object to Structure Modeller",
    version = "0.0.1",
    author = "Antonio Ribeiro",
    author_email = "alvesjunior.antonio@gmail.com",
    description = ("Tiny object to structure modeller."),
    license = "GPL",
    # keywords = "example documentation tutorial",
    url = "https://github.com/alvesjnr/tOSM",
    packages=['tosm',],
    long_description=read('README.md'),
)