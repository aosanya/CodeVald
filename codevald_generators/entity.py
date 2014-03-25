__author__ = 'Tony'

from codevald_generators import entityproperty

class entity():
    def __init__(self, a_name, a_properties=None):
        self.name = a_name
        if a_properties == None:
            self.properties = entityproperty.entitypropertylist()
        else:
            self.properties = a_properties