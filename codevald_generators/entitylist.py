__author__ = 'Tony'


class entitylist (list):

    def __init__(self):
        list.__init__([])

    def len(self):
        return len(self)

    def add(self, *args):
        self.extend(args)
        return None



    # @staticmethod
    # def sanitize(time_string):
    #     if '-' in time_string:
    #         splitter = '-'
    #     elif ':' in time_string:
    #         splitter = ':'
    #     else:
    #         return time_string
    #     (mins, secs) = time_string.split(splitter)
    #     return mins + '.' + secs

    # @property
    # def top3(self):
    #     return sorted(set([self.sanitize(t) for t in self]))[0:3]

    # @property
    # def clean_data(self):
    #     return sorted(set([self.sanitize(t) for t in self]))
