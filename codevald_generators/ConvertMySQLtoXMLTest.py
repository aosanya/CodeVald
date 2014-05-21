__author__ = 'Tony'

import os
from codevald_generators import MySQLtoXML
from codevald_generators import stringoperations

strPath = os.path.dirname(__file__) + "/../codevaldapp/data/"



filename = strPath + "sakila.sql"

MySQL = open(filename).read()

TempMySQL = MySQL.__str__()

NewXML = MySQLtoXML.MySQLtoXML(TempMySQL)

XML = NewXML.GetXML()

filename = strPath + "testsakila.xml"

f = open(filename, "w")
f.write(XML.__str__())
f.close()
