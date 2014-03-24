#! /usr/local/bin/python3
__author__ = 'Tony'

import yate
import cgitb
import cgi
from MySQLtoXML import MySQLtoXML
cgitb.enable()

form = cgi.FieldStorage()

#strPath = os.path.dirname(__file__)+"/../datamodels/"

#filename = strPath + "test.txt"

#f = open(filename, "w")

NewXML = MySQLtoXML('')
for each_form_item in form.keys():
    if each_form_item == "txtMySQL":
        NewXML = MySQLtoXML(form["txtMySQL"].value)
    break

if NewXML.script != "":
    form["txtMySQL"].value = NewXML.GetXML()
    #form["txtXML"].value = "wilre!"


#f.close()
page = ""
page = page + (yate.start_response())
page = page + (yate.include_header("CodeVald | MySql -> XML"))

#Menu
page = page + (yate.addcontent('templates/menu_open.html'))
page = page + (yate.addcontent('templates/menu_body.html'))
page = page + (yate.addcontent('templates/menu_close.html'))
page = page + (yate.addcomment('END SIDEBAR'))
#End Menu
#Content
page = page + (yate.addcomment('BEGIN CONTENT'))
page = page + (yate.opendiv('page-content-wrapper'))
page = page + (yate.opendiv('page-content-wrapper'))
page = page + (yate.opendiv('page-content'))
page = page + (yate.addtitle("CodeVald", "MySql -> XML"))
page = page + (yate.addcomment('BEGIN PAGE CONTENT'))
page = page + (yate.addcomment('BEGIN Portlet PORTLET'))
Content = yate.addcontent('content/MySqltoXML.html')

page = page + (Content)
page = page + (yate.addcomment('END PAGE CONTENT'))
page = page + (yate.closediv())
page = page + (yate.closediv())
page = page + (yate.closediv())
page = page + (yate.addcomment('END CONTENT'))
page = page + (yate.closediv())
#End Content
#Footer
page = page + (yate.include_footer({"Home": "/index.html"}))
#End Footer

page = yate.setformvalues(page, form)
#convert = MySQLtoXML(form["txtMySQL"].value)
#xml = mySQLtoXML.GetXML


print(page)



