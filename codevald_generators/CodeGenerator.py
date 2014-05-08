__author__ = 'Tony'
import os
from bs4 import BeautifulSoup
#from entitylist import entitylist
#from entity import entity
#from entityproperty import entityproperty
#from entityproperty import entitypropertylist
from codevald_generators import stringoperations
import textwrap


#strNewLine = "@$@!#%#@@!!!!1"
strCodeLine = "@$@!#%#@@!!!!2"
strPyLine = "@$@!#%#@@!!!!3"
strNoCloseQuote = "@$@!#%#@@!!!!4"
strPreviousQuote = "@$@!#%#@@!!!!5"


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
        temp = self.codeobjects
        for each_object in temp:
            loops.append("<" + each_object + ">")
            loops.append("</" + each_object + ">")
        return loops

    @property
    def codetagsopen(self):
        loops = []
        temp = self.codeobjects
        for each_object in temp:
            loops.append("<" + each_object + ">")
        return loops

    @property
    def pycodegenerator(self):
        self.code = self.template
        #self.code = self.code.replace("\n", strNewLine)
        self.createpylines()
        self.writecode("codetorun1_0.txt", self.code)

        self.clean_up1()

        self.writecode("codetorun1_1_1.txt", self.code)
        for each_object in self.codeobjects:
            self.set_conditions(each_object)

        self.writecode("codetorun1.txt", self.code)

        self.addcodeappend1()

        self.writecode("codetorun2.txt", self.code)

        for each_object in self.codeobjects:
            self.set_entityproperties(each_object)

        self.writecode("codetorun3.txt", self.code)

        self.decorateobjects()

        self.writecode("codetorun4.txt", self.code)

        for each_object in self.codeobjects:
            self.indent(each_object)

        self.writecode("codetorun4_1.txt", self.code)

        for each_object in self.codeobjects:
            self.set_loops(each_object)

        self.writecode("codetorun4_2.txt", self.code)
        #self.set_loops("property")
        #self.set_entity_name()
        #self.set_property_name()
        #self.set_property_sub()
        #self.clean_up2()
        self.writecode("codetorun6.txt", self.code)
        #self.removeemptylines()
        self.writecode("codetorun7.txt", self.code)
        self.addcodeappend2()

        self.writecode("codetorun9.txt", self.code)
        self.removeobjectsdefinition()

        self.clean_up2()
        self.writecode("codetorun10.txt", self.code)

        return self.code

    def writecode(self, filename, content):
        strPath = os.path.dirname(__file__) + "/../codevaldapp/data/"
        filename = strPath + filename
        f = open(filename, "w")
        f.write(content)
        f.close()

    def set_loops(self, looptag):
        instances = stringoperations.string_instance(self.code, "<" + looptag + ">")
        newcode = self.code
        for each_instance in reversed(instances):
            newcode = newcode.replace("<" + looptag + ">", "<" + looptag + ">")
            newcode = newcode.replace("<" + looptag + ">", "for each_" + looptag + " in o_XML.entities('" + looptag + "'):")
            #newcode = newcode.replace("\n</" + looptag + ">\n", "")
            newcode = newcode.replace("</" + looptag + ">", "")
        self.code = newcode

    def set_conditions(self, looptag):
        instances = stringoperations.string_instance(self.code, "<" + looptag + ".", )
        for each_instance in reversed(instances):

            tag_start = stringoperations.string_oneinstance(self.code, ">", each_instance)

            opentag = self.code[each_instance:tag_start + 1]
            temptag = opentag.replace("/>", ">")
            if opentag == temptag:

                closetag = opentag.replace("<", "</")

                tag_close = stringoperations.string_oneinstance(self.code, closetag, each_instance)
                if tag_close != -1:
                    content = self.code[each_instance + opentag.__len__():tag_close]
                    fulltag = self.code[each_instance:tag_close + closetag.__len__()]
                    opentag = opentag.replace(">", "')")
                    newcode = strNoCloseQuote + content + "' " + opentag.replace("<" + looptag + ".", ' if ' + looptag + "XML.entityproperty('")
                    #newcode = newcode.replace(">", "')")
                    newcode = newcode + ' != "<#Error#>" else ""'
                    self.code = self.code.replace(fulltag, strPyLine + newcode)

    def set_entityproperties(self, looptag):
        instances = stringoperations.string_instance(self.code, "<" + looptag + ".", )

        for each_instance in reversed(instances):
            tag_close = stringoperations.string_oneinstance(self.code, "/>", each_instance)
            oldcode = self.code[each_instance:tag_close + 2]
            if oldcode != "":
                if self.IsProperty(oldcode):
                    newcode = oldcode.strip()
                    newcode = newcode.replace("<" + looptag + ".", looptag + "XML.entityproperty('")
                    newcode = newcode.replace("/>", "')")
                    #self.code = self.code.replace(oldcode, "' + " +  newcode + " + '")
                    self.code = stringoperations.replacephrase(self.code, oldcode, "' + " +  newcode + " + '", each_instance, 1)

    def IsProperty(self, tag):
        temp = tag
        if temp[:1] != "<":
            return False

        if temp[-2:] != "/>":
            return False

        tempfound = False
        knowntags = []

        for each_object in self.codeobjects:
            knowntags.append("<" + each_object)

        if not stringoperations.startswith(tag.lstrip(" "), knowntags):
            return False

        return True


    #def set_property_sub(self):
    #    self.code = self.code.replace("<property.type\>", "\' + each_property.entityproperty('type') + \'")

    #def set_entity_name(self):
    #    self.code = self.code.replace("<entity\>", "\' + each_entity.entityproperty('name') + \'")

    #def set_property_name(self):
    #    self.code = self.code.replace("<property\>", "\' + each_property.entityproperty('name') + \'")

    #def clean_up(self):
    #    instances = stringoperations.string_instance(self.code, "<entity>")
    #    for each_instance in reversed(instances):
    #        entity_start = stringoperations.string_oneinstance(self.code, ">", each_instance)
    #        entity_close = stringoperations.string_oneinstance(self.code, "</entity>", each_instance)
    #        oldcode = self.code[entity_start+1:entity_close]
    #        newcode = oldcode.strip("\n")
    #        newcode = newcode.replace("\'", "\\'")
    #        newcode = newcode.replace("\n", "\\n")
    #        newcodelist = textwrap.wrap(newcode)
    #        newcode = ""
    #        for each_line in newcodelist:
    #            newcode = newcode + "\'" + each_line + "\'"
    #        newcode = "\n    codelist.append(" + newcode.strip() + ")"
    #        self.code = stringoperations.replacephrase(self.code, oldcode, newcode, entity_start, 1)

    def clean_up1(self):
        newcode = self.code

        for each_tag in self.codetagsopen:
            newcode = newcode.replace(each_tag, strPyLine + each_tag + strPyLine)
            newcode = newcode.replace(strPyLine + strPyLine + each_tag, strPyLine + each_tag)
            newcode = newcode.replace(each_tag + strPyLine + strPyLine, each_tag + strPyLine)

        newcode = newcode.replace("\'", strPreviousQuote)
        self.code = newcode

    def clean_up2(self):
        newcode = self.code
        newcode = newcode.replace(strPyLine, "\n")
        newcode = newcode.replace(strCodeLine, "\\n")
        newcode = newcode.replace(strPreviousQuote, "\\'")
        self.code = newcode

    def createpylines(self):
        newcode = self.code
        newcode = newcode.replace("\n", strPyLine)
        self.code = newcode

    def removeemptylines(self):
        loops = self.codetags
        newcode = self.code
        newcodelist = newcode.split("\n")
        newcode = ""
        for each_line in newcodelist:
            if each_line != "":
                newcode = newcode + "\n" + each_line

        newcode = newcode.replace(strPyLine, "\n")
        newcode = newcode.replace(strCodeLine, "\\n")
        self.code = newcode

    def addcodeappend1(self):
        loops = self.codetags

        checkloops = []
        for each_loop in loops:
            checkloops.append(each_loop)
            #checkloops.append(each_loop.replace(">", "."))

        checkloops.append("#objects")
        self.addcodeappendactual(checkloops)

    def addcodeappend2(self):
        loops = self.codetags

        checkloops = []
        for each_loop in loops:
            newtag = each_loop
            newtag = newtag.replace("<", "")
            newtag = newtag.replace(">", "")
            newtag = newtag + "XML"
            checkloops.append(newtag)

        checkloops.append("")
        checkloops.append("for each")
        checkloops.append("o_XML")
        checkloops.append("codelist.append")

        self.addcodeappendactual(checkloops)

    def addcodeappendactual(self, checkloops):
        checkloops.append("#objects")
        newcode = self.code
        newcodelist = newcode.split(strPyLine)
        newcode = ""
        for each_line in newcodelist:

            if not stringoperations.startswith(each_line.lstrip(" "), checkloops):
                NoClose = []
                NoClose.append(strNoCloseQuote)
                if not stringoperations.startswith(each_line.lstrip(" "), NoClose):
                    tempcode =  "codelist.append('" + strCodeLine + "<code>')"

                    tempcode = tempcode.replace("<code>", each_line.rstrip('\n'))
                    newcode = newcode + strPyLine + tempcode
                else:
                    tempcode =  "codelist.append('<code>)"

                    tempcode = tempcode.replace("<code>", each_line.rstrip('\n'))
                    tempcode = tempcode.replace(strNoCloseQuote, "")
                    newcode = newcode + strPyLine + tempcode
            else:
                tempcode = each_line
                newcode = newcode + strPyLine + tempcode

        self.code = newcode

    def indent(self, tag):
        instances = stringoperations.string_instance(self.code, "<" + tag + ">")
        for each_instance in reversed(instances):
            entity_start = stringoperations.string_oneinstance(self.code, ">", each_instance)
            entity_close = stringoperations.string_oneinstance(self.code, "</" + tag + ">", each_instance)
            oldcode = self.code[entity_start+1:entity_close]
            newcode = oldcode
            newcode = newcode.rstrip("\t")
            newcode = newcode.rstrip(strPyLine)
            newcode = newcode.replace(strPyLine, strPyLine + "    ")

            self.code = stringoperations.replacephrase(self.code, oldcode, newcode, entity_start, 1)

    def decorateobjects(self):
        for each_object in self.codeobjects:
            self.code = stringoperations.replacephrase(self.code, "<" + each_object + ">", "<" + each_object + ">" + strPyLine + each_object + "XML = ReadXML.ReadXML(each_" + each_object + ", True) " + strPyLine + "o_XML = " + each_object + "XML" + strPyLine, 0)

    def removeobjectsdefinition(self):
        objects_start = stringoperations.string_oneinstance(self.code, "#objects")
        objects_close = stringoperations.string_oneinstance(self.code, "]")
        if objects_start != -1 and objects_close != -1:
            tempobjects = self.code[objects_start:objects_close + "]".__len__()]
            objects = tempobjects.split(",")
            self.code = stringoperations.replacephrase(self.code, tempobjects, "", 0)
