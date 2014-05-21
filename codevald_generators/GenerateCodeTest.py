__author__ = 'Tony'

import os
from codevald_generators.ReadXML import ReadXML
from codevald_generators.CodeGenerator import GenerateCode
from bs4 import BeautifulSoup

strPath = os.path.dirname(__file__) + "/../codevaldapp/data/"

filename = strPath + "samplexml.xml"



template = strPath + "sampletemplate_vb3.txt"
o_template = open(template).read()
template_soup = BeautifulSoup(o_template)


o_GenerateCode = GenerateCode(o_template)
o_XMLPlain = open(filename).read()
o_XML = ReadXML(o_XMLPlain, [], "", False, o_GenerateCode.getmappers())

pycode = o_GenerateCode.pycodegenerator
codelist = []
#print(pycode)

filename = strPath + "codetorun.txt"

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

