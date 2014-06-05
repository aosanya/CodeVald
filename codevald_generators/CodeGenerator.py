__author__ = 'Tony'
import os
from bs4 import BeautifulSoup
import re
#from entitylist import entitylist
#from entity import entity
#from entityproperty import entityproperty
#from entityproperty import entitypropertylist
from codevald_generators import stringoperations
import textwrap
try:
    import urllib.request as urllib2
except:
    import urllib2

#strNewLine = "@$@!#%#@@!!!!1"
strCodeLine = "@$@!#%#@@!!!!2"
strPyLine = "@$@!#%#@@!!!!3"
strPyLineNoLine = "@$@!#%#@@!!!!3_121@##43"
strPyLineNoTemplateLine = "@$@!#%#@@!!!!2_121@##43"
strNoCloseQuote = "@$@!#%#@@!!!!4"
strPreviousQuote = "@$@!#%#@@!!!!5"
strPyIFLine = "1$@!#%5+@@!!!!6_1"
strPyIndent = "1$@!#%5+@@!!!!6_2"

class GenerateCode:
    def __init__(self, a_template):
        self.template = a_template
        self.code = ""
        self.template_soup = BeautifulSoup(self.template)
        self.links = self.template_soup.find_all('link')


    @property
    def codeobjects(self):
        template_soup = BeautifulSoup(self.template)
        objects_tags = template_soup.find_all('object')
        objects = []
        for each_object in objects_tags:
            objects.append(each_object["name"])

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
    def leftlinkobjects(self):
        objects = []
        for each_object in self.links:
            temp = each_object["left"]
            temp2 = temp.split(".")
            temp = ".".join(temp2[len(temp2) - 1])
            objects.append(temp)

        return objects

    def getcodetags(self, prefix, suffix):
        loops = []
        temp = self.codeobjects
        for each_object in temp:
            loops.append(prefix + each_object + suffix)
        return loops

    @property
    def pycodegenerator(self):
        self.code = self.template
        #self.code = self.code.replace("\n", strNewLine)
        #for each_object in self.codeobjects:

        self.clean_up_closetags()
        #self.writecode("codetorun1_0_2.txt", self.code.replace(strPyLine, "\n"))
        self.preset_loops()
        #self.writecode("codetorun1_0_3.txt", self.code.replace(strPyLine, "\n"))
        self.createpylines()
        #self.writecode("codetorun1_0_4.txt", self.code.replace(strPyLine, "\n"))
        #self.writecode("codetorun1_0_5.txt", self.code.replace(strPyLine, "\n"))
        self.clean_up1()

        #self.writecode("codetorun1_1_1.txt", self.code.replace(strPyLine, "\n"))
        self.set_conditions()

        #self.writecode("codetorun1.txt", self.code.replace(strPyLine, "\n"))

        self.addcodeappend1()

        #self.writecode("codetorun2.txt", self.code.replace(strPyLine, "\n"))

        for each_object in self.codeobjects:
            self.set_entityproperties(each_object.replace(strPyLine, "\n"))

        #self.writecode("codetorun3.txt", self.code.replace(strPyLine, "\n"))

        self.decorateobjects()

        #self.writecode("codetorun4.txt", self.code.replace(strPyLine, "\n"))

        for each_object in self.codeobjects:
            self.indent(each_object)

        #self.writecode("codetorun4_1.txt", self.code.replace(strPyLine, "\n"))

        for each_object in self.codeobjects:
            self.set_loops(each_object)

        #self.writecode("codetorun4_2.txt", self.code.replace(strPyLine, "\n"))
        #self.set_loops("property")
        #self.set_entity_name()
        #self.set_property_name()
        #self.set_property_sub()
        #self.clean_up2()
        #self.writecode("codetorun6.txt", self.code.replace(strPyLine, "\n"))
        #self.removeemptylines()
        #self.writecode("codetorun7.txt", self.code.replace(strPyLine, "\n"))
        self.addcodeappend2()

        #self.writecode("codetorun9.txt", self.code.replace(strPyLine, "\n"))

        self.end_clean_up_escapes()
        self.end_removeremaining_tags()

        self.addvariables()
        #self.writecode("codetorun10.txt", self.code.replace(strPyLine, "\n"))

        return self.code

    def writecode(self, filename, content):
        strPath = os.path.dirname(__file__) + "/../codevaldapp/data/"
        filename = strPath + filename
        f = open(filename, "w")
        f.write(content)
        f.close()

    def addvariables(self):
        self.code =  "o_XMLArray = []\n" + self.code

    def preset_loops(self):
        #soup = BeautifulSoup(self.template)
        #instances = soup.find_all(re.compile("^" + looptag +  "." + '(\s*?\S*?)*' + '>{1}'))

        instances = self.getcomplextags(self.code, self.codeobjects)
        newcode = self.code
        for each_instance in instances:
            opencode = ""
            closecode = ""
            prevclosetag = ""
            splitobject = each_instance[1:-1].split(".")
            loopcount = 0
            loopreset = False
            for objs in splitobject:
                subobjects = objs.split(' ')
                obj = subobjects[0]
                if obj in self.codeobjects:
                    prevtag = obj
                    opencode = opencode + "<" + objs + ">"
                    closecode =  "</" + obj + ">" + closecode
                    if prevclosetag == '':
                        prevclosetag = obj
                    else:
                        prevclosetag = prevclosetag + "." + obj
                    loopcount += 1
                else:
                    if loopcount > 1:
                        opencode = opencode + "<" + prevtag + "." + objs + "/>"
                        code_replacement = opencode + closecode
                        newcode = newcode.replace("<" + each_instance.name + "/>", code_replacement)

                    loopreset = True
                    break

            if not loopreset:
                code_replacement = opencode + strPyLineNoLine
                newcode = newcode.replace(each_instance, code_replacement)
                newcode = newcode.replace("</" + prevclosetag + ">", closecode)

        self.template = newcode
        self.code = newcode

    def set_loops(self, looptag):
        newcode = self.code
        objects = []
        objects.append(looptag)

        opentags = self.getopentags(self.code, objects)
        for each_tag in opentags:
            newcode = newcode.replace(each_tag, "for each_" + looptag + " in o_XML.entities('" + looptag + "'):")
            #newcode = newcode.replace("\n</" + looptag + ">\n", "")
            newcode = newcode.replace("</" + looptag + ">", "")
        self.code = newcode

    def set_conditions(self):
        newcode = self.code
        conditional_tags = self.getopentags_coditional(self.code, self.codeobjects)
        for each_instance in conditional_tags:
            splitobject = each_instance[1:-1].split(".")
            fullproperty = each_instance[1:-1]
            looptag = ".".join(splitobject[:len(splitobject) - 1])
            property = splitobject[-1]


            newcode = strPyIFLine + 'if ' + looptag + "XML.entityproperty('" + property + "')"
            newcode = newcode + ' != "<#Error#>":' + strPyIndent + strPyLine
            self.code = self.code.replace(each_instance, strPyLine + newcode)


    def set_conditionsold(self, looptag):
        soup = BeautifulSoup(self.template)
        instances = soup.find_all(re.compile("^" + looptag +  "."))
        newcode = self.code
        for each_instance in instances:
            fullproperty = ""
            closecode = ""
            splitobject = each_instance.name.split(".")
            loopcount = 0
            looptag = ""
            for obj in splitobject:
                if obj in self.codeobjects:
                    fullproperty = fullproperty + "." + obj
                    loopcount += 1
                else:
                    looptag = fullproperty
                    property = obj
                    fullproperty = fullproperty + "." + obj

                    fulltag = "<" + fullproperty + "/>"
                    newcode = strNoCloseQuote + fullproperty + "' " + ' if ' + looptag + "XML.entityproperty('" + property + "')"
                    newcode = newcode + ' != "<#Error#>" else ""'
                    self.code = self.code.replace(fulltag, strPyLine + newcode)

                    break

    def set_conditions2(self, looptag):
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


        instances = self.getopentags(self.template, self.codeobjects)

        for each_instance in reversed(instances):
            newcode = newcode.replace(each_instance, strPyLine + each_instance + strPyLine)
            newcode = newcode.replace(strPyLine + strPyLine + each_instance, strPyLine + each_instance)
            newcode = newcode.replace(each_instance + strPyLine + strPyLine, each_instance + strPyLine)

        closetags = self.getCloseTags(self.code, self.codeobjects)
        for each_tag in closetags:
            newcode = newcode.replace(each_tag, strPyLine + each_tag)
            newcode = newcode.replace(strPyLine + strPyLine + each_tag, strPyLine + each_tag)

        newcode = newcode.replace("\'", strPreviousQuote)
        self.code = newcode

    def clean_up_closetags(self):
        newcode = self.code
        closetags = self.getCloseTags(self.code, self.codeobjects)
        for each_tag in closetags:

            new_tag = each_tag.replace(" ", "")

            newcode = newcode.replace(each_tag, strPyLine + new_tag)
            newcode = newcode.replace(strPyLine + strPyLine + new_tag, strPyLine + new_tag)

        self.code = newcode

    def end_clean_up_escapes(self):
        self.removeobjectsdefinition("object")
        self.removeobjectsdefinition("link")
        self.removeobjectsdefinition("mapper")

        newcode = self.code

        newcode = newcode.replace(strPyLineNoTemplateLine, "")
        newcode = newcode.replace(strPyIndent + strPyLine, "\n\t")
        newcode = newcode.replace(strPyLine, "\n")
        newcode = newcode.replace(strCodeLine, "\\n")
        newcode = newcode.replace(strPreviousQuote, "\\'")
        newcode = newcode.replace(strPyIFLine, "")
        self.code = newcode

    def createpylines(self):
        newcode = self.code
        newcode = newcode.replace("\n", strPyLine)
        closetags = self.getCloseTags(self.code, self.codeobjects)
        for each_tag in closetags:
            newcode = newcode.replace(each_tag, each_tag + strPyLineNoLine)
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

    def end_removeremaining_tags(self):
        newcode = self.code
        closetags = self.getCloseTags(self.code, self.codeobjects)
        for each_tag in closetags:
            newcode = newcode.replace(each_tag, "")
        self.code = newcode

    def addcodeappend1(self):
        opentags = self.getopentags(self.template, self.codeobjects)
        #opentags = self.getopentagsregex(self.template, self.codeobjects)
        closetags = self.getCloseTags(self.code, self.codeobjects)

        checkloops = opentags + closetags
        checkloops.append(strPyIFLine)
        self.addcodeappendactual(checkloops, opentags, closetags)

    def addcodeappend2(self):
        loops = self.codetags

        checkloops = []
        for each_loop in loops:
            newtag = each_loop
            newtag = newtag.replace("<", "")
            newtag = newtag.replace(">", "")
            newtag = newtag
            checkloops.append(newtag + "XML")
            checkloops.append(newtag + "index =")

        checkloops.append("")
        checkloops.append("for each")
        checkloops.append("o_XML")
        checkloops.append("codelist.append")

        opentags = self.getopentags(self.template, self.codeobjects)
        closetags = self.getCloseTags(self.code, self.codeobjects)

        self.addcodeappendactual(checkloops, opentags, closetags)

    def addcodeappendactual(self, checkloops, opentags, closetags):
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
        objects = []
        objects.append(tag)
        opentags = self.getopentags(self.template, objects)
        for each_opentag in opentags:
            instances = stringoperations.string_instance(self.code, each_opentag)
            for each_instance in reversed(instances):
                entity_close = stringoperations.string_oneinstance(self.code, "</" + tag + ">", each_instance)
                oldcode = self.code[each_instance:entity_close]
                newcode = oldcode
                newcode = newcode.rstrip("\t")
                newcode = newcode.rstrip(strPyLine)
                newcode = newcode.replace(strPyLine, strPyLine + "    ")

                self.code = stringoperations.replacephrase(self.code, oldcode, newcode, each_instance, 1)

    def decorateobjects(self):

        contionaltags = self.getopentags_coditional(self.code, self.codeobjects)
        for each_object in self.codeobjects:
            objects = []
            objects.append(each_object)
            opentags = self.getopentags(self.code, objects)
            for each_opentag in opentags:
                #if each_opentag not in contionaltags:
                self.code = stringoperations.replacephrase(self.code, each_opentag, strPyLine + each_object + "index = 0" + strPyLine + each_object + "count = len(o_XML.entities('" + each_object + "'))" + strPyLine + each_opentag + strPyLine + each_object + "XML = ReadXML.ReadXML(each_" + each_object + ", o_GenerateCode.codeobjects, o_GenerateCode.links, True, o_GenerateCode.getmappers()) " + strPyLine + "o_XML = " + each_object + "XML" + strPyLine + "o_XMLArray.append(o_XML)" + strPyLine, 0)

                instances = stringoperations.string_instance(self.code, each_opentag)
                separator = ""
                separator = self.getattribute(each_opentag, "separator")

                for each_instance in reversed(instances):
                    tag_close = stringoperations.string_oneinstance(self.code, "</" + each_object + ">", each_instance)

                    if tag_close != -1:
                        self.code = stringoperations.replacephrase(self.code, "</" + each_object + ">", strPyLine + each_object + "index += 1" + strPyLine + "if " + each_object + "index < " + each_object + "count:" + strPyLine + "\tcodelist.append('" + separator + "')" + strPyLine + "o_XMLArray.pop()" + strPyLine + "if len(o_XMLArray)>0:" + strPyLine + "\to_XML = o_XMLArray[-1]" + strPyLine + "</" + each_object + ">", each_instance ,1)
                self.code = self.code.replace(each_opentag, "<" + each_object + ">")

    def removeobjectsdefinition(self, object):
        instances = stringoperations.string_instance(self.code, "#<" + object)

        for each_instance in reversed(instances):
            objects_close = stringoperations.string_oneinstance(self.code, "/>", each_instance)
            if objects_close != -1:
                tempobjects = self.code[each_instance:objects_close + "/>".__len__()]
                self.code = stringoperations.replacephrase(self.code, tempobjects + strCodeLine, "", 0)
                self.code = stringoperations.replacephrase(self.code, strCodeLine + tempobjects, "", 0)
                self.code = stringoperations.replacephrase(self.code, tempobjects, "", 0)

    def getattribute(self, xml, attribute):
        try:
            xml = re.sub('<\s*', '<', xml)
            soup = BeautifulSoup(xml)
            for each in soup:
                valAtt = each[attribute]
                break
        except:
            valAtt = ""
        return valAtt

    def getinstances(self, xml, object):
        soup = BeautifulSoup(xml)
        instances = soup.find_all(object)

        return instances

    def gettags(self, xml, objects):
        Tags = []

        for each_obj in objects:
            p = re.compile('<\s*' + each_obj + '(\s*?\S*?)*' + '>{1}')

            iterator = p.finditer(xml)
            for match in iterator:
                Tags.append(match.group())

        return Tags

    def getopentags2(self, xml, objects):
        Tags = []
        instances = self.getinstances(xml, objects)
        for each_instance in instances:
            strInstance = each_instance.__str__()
            Tag = self.getregex(strInstance, ".*?>")
            Temp = Tag.replace("/>", ">")
            if Tag == Temp:
                Tags.append(Tag)
        return Tags

    def getregex(self, phrase, filter):
        p = re.compile(filter)
        iterator = p.finditer(phrase)
        for match in iterator:
            return match.group()

        return ""

    def getopentags(self, xml, objects):

        Tags = []
        for each_obj in objects:
            ps = []

            ps.append(re.compile('<\s*' + each_obj + '\s+.*?' + '>'))
            ps.append(re.compile('<\s*' + each_obj + '\s*' + '>'))

            for p in ps:
                #p = re.compile('<\s*' + each_obj + " " + '(\s*?\S*?)*' + '>{1}')
                iterator = p.finditer(xml)
                for match in iterator:
                    temp = match.group()
                    temp = temp.replace("/>", ">")
                    temp = temp.replace("</", "<")
                    if temp == match.group():
                        if temp not in Tags:
                            Tags.append(match.group())

        return Tags

    def getopentags_coditional(self, xml, objects):
        Tags = []

        for each_obj in objects:
            #p = re.compile('<\s*' + each_obj + '((\s*\w*"*)*' + "(\s*\w*'*)*)>")
            p = re.compile('<\s*' + each_obj + '(\s*?\S*?)*' + '>{1}')

            iterator = p.finditer(xml)
            for match in iterator:
                temp = match.group()
                temp = temp.replace("/>", ">")
                temp = temp.replace("</", "<")
                if temp == match.group():
                    try:
                        foundspace = temp.index(" ", 0)
                    except:
                        foundspace = -1

                    if foundspace == -1:
                        actualtag = temp[1:-1]
                        actuals = actualtag.split(".")
                        if len(actuals) > 1:
                            if actuals[len(actuals)-1] not in objects:
                                if temp not in Tags:
                                    Tags.append(match.group())

        return Tags

    def getCloseTags(self, xml, objects):
        Tags = []

        for each_obj in objects:
            p = re.compile('</\s*' + each_obj  + '(\s*?\S*?)*' + '>{1}')

            iterator = p.finditer(xml)
            for match in iterator:
                temp = match.group()
                if temp not in Tags:
                    Tags.append(match.group())

        return Tags

    def getcomplextags(self, xml, objects):
        Tags = []

        for each_obj in objects:
            p = re.compile('<{1}\s*' + each_obj + '\.(\s*?\S*?)*' + '>{1}')

            iterator = p.finditer(xml)
            for match in iterator:
                Tags.append(match.group())

        return Tags

    def getmappers(self):
        Tags = []

        soup = BeautifulSoup(self.template)

        mappers = soup.find_all("mapper")

        varMaps = []
        for each_mapper in mappers:
            try:
                thefrom = each_mapper["from"]
                theto = each_mapper["from"]
                varMap = [each_mapper["object"], each_mapper["property"], each_mapper["from"], each_mapper["to"]]
                varMaps.append(varMap)
            except:
                pass

        return varMaps