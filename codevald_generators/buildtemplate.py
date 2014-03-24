__author__ = 'Tony'
import os
from bs4 import BeautifulSoup
#from entitylist import entitylist
#from entity import entity
#from entityproperty import entityproperty
#from entityproperty import entitypropertylist
import stringoperations

strPath = os.path.dirname(__file__)+"/../datamodels/"

class buildtemplate:
    def __init__(self, a_template):
        self.template = a_template
        self.code = ""


    @property
    def pycode(self):

        self.code = self.template
        self.clean_up()
        self.set_entity_loops()
        self.set_entity_name()
        return self.code


    def set_entity_loops(self):
        self.code = self.code.replace("<entity>", "\nfor each_entity in o_ReadXML.entities:")
        self.code = self.code.replace("</entity>", "")


    def set_entity_name(self):
        self.code = self.code.replace("<entity\>", "\' + each_entity.name + \'")


    def clean_up(self):
        instances = stringoperations.string_instance(self.code, "<entity>")
        for each_instance in reversed(instances):
            entity_start = stringoperations.string_oneinstance(self.code, ">", each_instance)
            entity_close = stringoperations.string_oneinstance(self.code, "</entity>", each_instance)
            oldcode = self.code[entity_start+1:entity_close]
            newcode = oldcode.strip("\n")
            newcode = oldcode.replace("\n", "\\n")
            newcode = "\n\tcode.append(\'" + newcode.strip() + "\')\n"
            self.code = stringoperations.replacephrase(self.code, oldcode, newcode, entity_start, 1)


    #def add_variables(self):
