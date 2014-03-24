__author__ = 'Tony'

import os
from ReadXML import ReadXML
from buildtemplate import buildtemplate
from entity import entity

strPath = os.path.dirname(__file__)+"/../datamodels/"

filename = strPath + "Sakila.xml"

o_XML = open(filename).read()
o_ReadXML = ReadXML(o_XML)

template = strPath + "blltemplate.txt"
o_template = open(template).read()

o_buildtemplate = buildtemplate(o_template)
pycode = o_buildtemplate.pycode
code = []
#print(pycode)

filename = strPath + "codetorun.txt"

f = open(filename, "w")
f.write(pycode)
f.close()







filename = strPath + "code.txt"

exec(pycode)
f = open(filename, "w")
for each_code in code:
    f.write(each_code)
f.close()

#exec(o_template)

#for each_entity in o_ReadXML.entities:
#    print (each_entity.name)