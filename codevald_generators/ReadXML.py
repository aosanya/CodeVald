__author__ = 'Tony'
import os
from bs4 import BeautifulSoup
from codevald_generators import entitylist
from codevald_generators import entity
from codevald_generators import entityproperty

strPath = os.path.dirname(__file__)+"/../datamodels/"


class ReadXML:
    def __init__(self, a_XML, a_souped = False):
        self.XML = a_XML
        self.souped = a_souped

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


    def entities(self, entitytag):
        if self.souped == False:
            soup = BeautifulSoup(self.XML)
            self.souped = True
            entities_xml = soup.find_all(entitytag)
        else:
            entities_xml = self.XML.find_all(entitytag)

        return entities_xml

    def entityproperty(self, property):
        try:
            return self.XML[property]
        except:
            return "<#Error#>"