__author__ = 'Tony'

import os
from codevald_generators.ReadXML import ReadXML
from codevald_generators.CodeGenerator import GenerateCode
from codevald_generators.entity import entity

strPath = os.path.dirname(__file__)+"/../datamodels/"

filename = strPath + "xml2.txt"

o_XMLPlain = open(filename).read()
o_XML = ReadXML(o_XMLPlain)

template = strPath + "template2.txt"
o_template = open(template).read()

o_GenerateCode = GenerateCode(o_template)
pycode = o_GenerateCode.pycodegenerator
codelist = []
#print(pycode)

filename = strPath + "codetorun4.txt"

f = open(filename, "w")
f.write(pycode)
f.close()

filename = strPath + "code.txt"


exec(pycode)
f = open(filename, "w")
for each_code in codelist:
    f.write(each_code)
f.close()

#exec(o_template)

#for each_entity in o_ReadXML.entities:
#    print (each_entity.name)

