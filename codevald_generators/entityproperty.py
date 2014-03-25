__author__ = 'Tony'


class entityproperty():
    def __init__(self, a_name):
        self.name = a_name


class entitypropertylist(list):

    def __init__(self):
        list.__init__([])

    def len(self):
        return len(self)

    def add(self, *args):
        self.extend(args)
        return None