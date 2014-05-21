__author__ = 'Tony'
import os
from bs4 import BeautifulSoup
from codevald_generators import entitylist
from codevald_generators import entity
from codevald_generators import entityproperty

strPath = os.path.dirname(__file__)+"/../datamodels/"


class ReadXML:

    def __init__(self, a_XML, objects, links, a_souped = False, a_mappers = []):
        self.XML = a_XML
        self.IsSouped = a_souped
        self.links = links
        self.objects = objects
        self.mappers = a_mappers

    #@property
    #def entities(self):
    #    soup = BeautifulSoup(self.XML)
    #    entities_xml = soup.find_all('entity')
    #    o_entitylist = entitylist.entitylist()
    #    for each_entity_xml in entities_xml:
    #        o_entity = entity.entity(each_entity_xml['name'])
    #        propertylist_xml = each_entity_xml.find_all('property')
    #        o_entitylist.properties = entityproperty.entitypropertylist()
    #        for each_property_xml in propertylist_xml:
    #            propname = each_property_xml['name']
    #            o_property = entityproperty.entityproperty(each_property_xml['name'])
    #            props = o_entity.properties
    #            o_entity.properties.append(o_property)
    #            props = o_entity.properties
    #        o_entitylist.add(o_entity)
    #    return o_entitylist

    #@property
    def soup(self):
        if not self.IsSouped:
            soup = BeautifulSoup(self.XML)
        else:
            soup = self.XML

        return soup

    def entities(self, entitytag):
        if self.IsSouped == False:
            soup = BeautifulSoup(self.XML)
            entities_xml = soup.find_all(entitytag)
        else:
            entities_xml = self.XML.find_all(entitytag)

        return entities_xml

    def entityproperty(self, property):
        value = ""
        try:
            value = self.XML[property]
        except:
            value = ""

        if value == "":
            fullparent = ""
            for parent in self.XML.parents:
                if parent.name in self.objects:
                    fullparent = parent.name + "." + fullparent
            fullparent = fullparent + self.XML.name

            if fullparent in self.rightlinkobjects():
                for each_right in self.rightlinkproperties(fullparent):
                    IDName = each_right.split(".")
                    IDName = IDName[-1:]
                    IDName2 = IDName[0]

                    IDValue = self.XML[IDName2]

                    for each_left in self.leftlinkproperties("", each_right):
                        value = self.GetObject(self.XML, each_left, IDValue, property)

        if value == "":
            value = "<#Error#>"

        for each_map in self.mappers:
            if each_map[0] == self.XML.name and each_map[1] == property and each_map[2].lower() == value.lower():
                value = each_map[3]

        return value


    def leftlinkobjects(self):
        objects = []
        for each_object in self.links:
            temp = each_object["left"]
            temp2 = temp.split(".")
            temp2 = ".".join(temp2[:len(temp2) - 1])
            objects.append(temp)

        return objects

    def rightlinkobjects(self):
        objects = []
        for each_object in self.links:
            temp = each_object["right"]
            temp2 = temp.split(".")
            temp2 = ".".join(temp2[:len(temp2) - 1])
            objects.append(temp2)

        return objects

    def rightlinkproperties(self, object = "", left = ""):
        objects = []
        for each_object in self.links:
            temp = each_object["right"]
            temp2 = temp.split(".")
            temp2 = ".".join(temp2[:len(temp2) - 1])
            if temp2 == object or each_object["right"] == left:
                objects.append(temp)

        return objects

    def leftlinkproperties(self, object ="", right = ""):
        objects = []
        for each_object in self.links:
            temp = each_object["left"]
            temp2 = temp.split(".")
            temp2 = ".".join(temp2[:len(temp2) - 1])
            if temp2 == object or each_object["right"] == right:
                objects.append(temp)

        return objects

    def GetObject(self, XML, Path, IDValue, Property):
        hasparent=True
        currParent = XML
        while hasparent:
            tempParent = currParent.parent
            if tempParent.name in self.objects:
                currParent = tempParent
            else:
                break

        varPathSplit = Path.split(".")
        varPathSplit2 = varPathSplit[1:-1]
        IDProperty = varPathSplit[-1:]
        IDProperty = IDProperty[0]
        #for each_object in currParent.find_all(varPathSplit2):
        value = self.GetSubObject(currParent, varPathSplit2, IDProperty, IDValue, Property)
        return value

    def GetSubObject(self, XML, Path, IDProperty, IDValue, Property):
        varPathSplit2 = Path[1:-1]

        if len(varPathSplit2) == 0:
            LastProperty = Path[0]
            for each_obj in XML.find_all(LastProperty):
                if each_obj[IDProperty] == IDValue:
                    value = each_obj[Property]
                    break
        else:
            for each_object in XML.find_all(Path):
                value = self.GetSubObject(each_object, varPathSplit2, IDProperty)

        return value