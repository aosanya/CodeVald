__author__ = 'Tony'
import os
from bs4 import BeautifulSoup
#from entitylist import entitylist
#from entity import entity
#from entityproperty import entityproperty
#from entityproperty import entitypropertylist
from codevald_generators import stringoperations
import textwrap
strPath = os.path.dirname(__file__)+"/../datamodels/"

strNewLine = "@$@!#%#@@!!!!3424"
class GenerateCode:
    def __init__(self, a_template):
        self.template = a_template
        self.code = ""

    @property
    def codeobjects(self):
        objects_start = stringoperations.string_oneinstance(self.code, "#objects")
        objects_close = stringoperations.string_oneinstance(self.code, "]")
        if objects_start == -1 or objects_close == -1:
            return ""

        tempobjects = self.code[objects_start+1:objects_close]

        objects_start = stringoperations.string_oneinstance(self.code, "[")

        if objects_start == -1:
            return ""

        tempobjects = self.code[objects_start+1:objects_close]

        objects = tempobjects.split(",")

        return objects
    @property
    def codetags(self):
        loops = []
        for each_object in self.codeobjects:
            loops.append("<" + each_object + ">")
            loops.append("</" + each_object + ">")
        return loops

    @property
    def pycodegenerator(self):
        self.code = self.template
        self.code.replace("\n", strNewLine)

        filename = strPath + "codestate1.txt"
        f = open(filename, "w")
        f.write(self.code)
        f.close()


        self.clean_up2()

        filename = strPath + "codestate2.txt"
        f = open(filename, "w")
        f.write(self.code)
        f.close()

        self.addcodeappend()
        filename = strPath + "codestate3.txt"
        f = open(filename, "w")
        f.write(self.code)
        f.close()

        self.decorateobjects()
        self.indent("entity")
        self.indent("property")
        for each_object in self.codeobjects:
            self.set_loops(each_object)

        for each_object in self.codeobjects:
            self.set_entityproperties(each_object)

        #self.set_loops("property")
        #self.set_entity_name()
        #self.set_property_name()
        #self.set_property_sub()
        self.removeemptylines()
        self.code.replace(strNewLine, "\n")
        self.removeobjectsdefinition()
        return self.code

    def set_loops(self, looptag):
        instances = stringoperations.string_instance(self.code, "<" + looptag + ">")
        for each_instance in reversed(instances):
            self.code = self.code.replace("<" + looptag + ">", "for each_" + looptag + " in o_XML.entities('" + looptag + "'):")
            self.code = self.code.replace("</" + looptag + ">", "")

    def set_entityproperties(self, looptag):
        instances = stringoperations.string_instance(self.code, "<" + looptag + ".", )
        for each_instance in reversed(instances):
            tag_close = stringoperations.string_oneinstance(self.code, "\>", each_instance)
            oldcode = self.code[each_instance:tag_close + 2]
            newcode = oldcode.strip()
            newcode = newcode.replace("<" + looptag + ".", looptag + "XML.entityproperty('")
            newcode = newcode.replace("\>", "')")
            self.code = self.code.replace(oldcode, "' + " +  newcode + " + '")

    #def set_property_sub(self):
    #    self.code = self.code.replace("<property.type\>", "\' + each_property.entityproperty('type') + \'")

    #def set_entity_name(self):
    #    self.code = self.code.replace("<entity\>", "\' + each_entity.entityproperty('name') + \'")

    #def set_property_name(self):
    #    self.code = self.code.replace("<property\>", "\' + each_property.entityproperty('name') + \'")

    def clean_up(self):
        instances = stringoperations.string_instance(self.code, "<entity>")
        for each_instance in reversed(instances):
            entity_start = stringoperations.string_oneinstance(self.code, ">", each_instance)
            entity_close = stringoperations.string_oneinstance(self.code, "</entity>", each_instance)
            oldcode = self.code[entity_start+1:entity_close]
            newcode = oldcode.strip("\n")
            newcode = newcode.replace("\'", "\\'")
            newcode = newcode.replace("\n", "\\n")
            newcodelist = textwrap.wrap(newcode)
            newcode = ""
            for each_line in newcodelist:
                newcode = newcode + "\'" + each_line + "\'"
            newcode = "\n    codelist.append(" + newcode.strip() + ")"
            self.code = stringoperations.replacephrase(self.code, oldcode, newcode, entity_start, 1)

    def clean_up2(self):
        newcode = self.code
        newcode = newcode.replace("<entity>", "\n<entity>")
        newcode = newcode.replace("<property>", "\n<property>")
        #newcode = newcode.replace("</entity>", "\n</entity>")
        #newcode = newcode.replace("</property>", "\n</property>")

        self.code = newcode

    def removeemptylines(self):
        loops = self.codetags
        newcode = self.code
        newcodelist = newcode.split("\n")
        newcode = ""
        for each_line in newcodelist:
            if each_line != "":
                newcode = newcode + "\n" + each_line

        newcode = newcode.replace("codelist.append('", "codelist.append('\\n")
        self.code = newcode

    def addcodeappend(self):
        loops = self.codetags

        loops.append("#objects")
        newcode = self.code
        seperator = "@$#%Q$VCSv"
        newcode = newcode.replace("\n", seperator)
        newcodelist = newcode.split(seperator)
        newcode = ""
        for each_line in newcodelist:

            if not stringoperations.startswith(each_line, loops):
                tempcode =  "codelist.append('<code>')"

                tempcode = tempcode.replace("<code>", each_line[0:-1])
                newcode = newcode + tempcode + "\n"
            else:
                tempcode = each_line
                newcode = newcode + tempcode + "\n"

        self.code = newcode


    def indent(self, tag):
        instances = stringoperations.string_instance(self.code, "<" + tag + ">")
        for each_instance in reversed(instances):
            entity_start = stringoperations.string_oneinstance(self.code, ">", each_instance)
            entity_close = stringoperations.string_oneinstance(self.code, "</" + tag + ">", each_instance)
            oldcode = self.code[entity_start+1:entity_close]
            newcode = oldcode
            newcode = newcode.rstrip("\t")
            newcode = newcode.rstrip("\n")
            newcode = newcode.replace("\n", "\n    ")
            #newcodelist = newcode.split("\n")
            #newcode = ""
            #for each_line in newcodelist:
            #newcode = newcode + "\n"

            self.code = stringoperations.replacephrase(self.code, oldcode, newcode, entity_start, 1)

    def decorateobjects(self):
        for each_object in self.codeobjects:
            self.code = stringoperations.replacephrase(self.code, "<" + each_object + ">", "<" + each_object + ">\n" + each_object + "XML = ReadXML.ReadXML(each_" + each_object + ", True)\no_XML = " + each_object + "XML\n", 0)

    def removeobjectsdefinition(self):
        objects_start = stringoperations.string_oneinstance(self.code, "#objects")
        objects_close = stringoperations.string_oneinstance(self.code, "]")
        if objects_start != -1 and objects_close != -1:
            tempobjects = self.code[objects_start:objects_close + "]".__len__()]
            objects = tempobjects.split(",")
            self.code = stringoperations.replacephrase(self.code, tempobjects, "", 0)
