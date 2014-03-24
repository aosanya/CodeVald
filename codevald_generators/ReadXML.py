__author__ = 'Tony'
import os
from bs4 import BeautifulSoup
from entitylist import entitylist
from entity import entity
from entityproperty import entityproperty
from entityproperty import entitypropertylist

strPath = os.path.dirname(__file__)+"/../datamodels/"

class ReadXML:
    def __init__(self, a_XML):
        self.XML = a_XML


    @property
    def entities(self):
        soup = BeautifulSoup(self.XML)
        entities_xml = soup.find_all('entity')
        o_entitylist = entitylist()
        for each_entity_xml in entities_xml:
            o_entity = entity(each_entity_xml['name'])
            propertylist_xml = each_entity_xml.find_all('property')
            o_entitylist.properties = entitypropertylist()
            for each_property_xml in propertylist_xml:
                propname = each_property_xml['name']
                o_property = entityproperty(each_property_xml['name'])
                props = o_entity.properties
                o_entity.properties.append(o_property)
                props = o_entity.properties
            o_entitylist.add(o_entity)
        return o_entitylist