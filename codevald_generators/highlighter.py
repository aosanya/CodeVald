__author__ = 'Tony'
import os
from bs4 import BeautifulSoup
from codevald_generators import stringoperations
import textwrap
strPath = os.path.dirname(__file__)+"/../datamodels/"

strNewLine = "@$@!#%#@@!!!!3424"
class highlighter:
    def __init__(self, text):
        self.text = text

    @property
    def codeobjects(self):
        objects_start = stringoperations.string_oneinstance(self.text, "#objects")
        objects_close = stringoperations.string_oneinstance(self.text, "]")
        if objects_start == -1 or objects_close == -1:
            return ""

        tempobjects = self.text[objects_start+1:objects_close]

        objects_start = stringoperations.string_oneinstance(self.text, "[")

        if objects_start == -1:
            return ""

        tempobjects = self.text[objects_start+1:objects_close]

        objects = tempobjects.split(",")

        return objects
    @property
    def codetags(self):
        loops = []
        for each_object in self.codeobjects:
            loops.append("<" + each_object + ">")
            loops.append("</" + each_object + ">")
        return loops

    def highlight(self):
        loops = self.codetags

        for each_tag in loops:
            self.text = stringoperations.highlight(self.text, each_tag, "red")

        return self.text