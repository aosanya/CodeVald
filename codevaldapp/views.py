from django.shortcuts import render
from django.shortcuts import render_to_response
from django.templatetags.static import static
from django.template import Template, Context, RequestContext
from codevald_generators import MySQLtoXML
from codevald_generators import ReadXML
from codevald_generators import CodeGenerator
import cgitb
import os
from inspect import stack, getmodule

cgitb.enable


def ContextWithView(request):
    """Template context with current_view value,
    a string with the full namespaced django view in use.
    """
    # Frame 0 is the current frame
    # So assuming normal usage the frame of the view
    # calling this processor should be Frame 1
    name = getmodule(stack()[1][0]).__name__
    return {
        'current_view': "%s.%s" % (name, stack()[1][3]),
    }


def GetMenu(currentview):
    content = open('codevaldapp/static/codevaldapp/assets/content/menu.html', 'r+')
    t = Template(content.read())
    c = Context({"currentview": currentview})
    content.close()
    menu = t.render(c)
    return menu


def index(request):
    menu = GetMenu("codevaldapp:index")
    content = open('codevaldapp/static/codevaldapp/assets/content/home.html', 'r+')
    t = Template(content.read())
    c = Context({})
    content.close()
    html = t.render(c)
    return render(request, 'codevaldapp/template.html', {"title": "CodeVald : Home", "pagetitle": "CodeVald", "pagesubtitle": "XML + Template = (formative) Code", "menu": menu, "content": html})


def Team(request):
    menu = GetMenu("codevaldapp:Team")
    content = open('codevaldapp/static/codevaldapp/assets/content/team.html', 'r+')
    t = Template(content.read())
    c = Context({})
    content.close()
    html = t.render(c)	

    return render(request, 'codevaldapp/template.html', {"title": "CodeVald : Team", "pagetitle": "Team", "pagesubtitle": "", "CurrPage": "Team", "menu": menu, "content": html})


def ConvertMySQLToXML(request):
    menu = GetMenu("codevaldapp:MySQLToXML")
    if request.method == "POST":
        message = "Script not converted"
        messageclass = "msgerror"
        try:
            MySQL = request.POST['txtMySQL']
        except:
            MySQL = ""
            XML = ""

        if MySQL != "":
            NewXML = MySQLtoXML.MySQLtoXML(MySQL)
            XML = NewXML.GetXML
            messageclass = "msgsuccess"
            message = "Process Complete!"

        content = open('codevaldapp/static/codevaldapp/assets/content/MySQLToXML.html', 'r+')
        t = Template(content.read())
        c = Context({"activetab": "XML", "MySQL": MySQL, "XML": XML, "message": message, "messageclass": messageclass})
        content.close()
        html = t.render(c)

        return render_to_response('codevaldapp/template_form.html', {"title": "CodeVald : Convert SQL", "action": "codevaldapp:MySQLToXML", "pagetitle": "Generate XML", "pagesubtitle": "MySQL to XML", "CurrPage": "Generate XML", "menu": menu, "content": html}, context_instance=RequestContext(request))
    else:
        content = open('codevaldapp/static/codevaldapp/assets/content/MySQLToXML.html', 'r+')
        sampleMySQL = open('codevaldapp/data/sakila.sql', 'r+')
        sampleMySQL = sampleMySQL.read()
        MySQL = sampleMySQL.__str__()
        t = Template(content.read())
        c = Context({"activetab": "MySQL", "MySQL": MySQL, "XML": ""})
        content.close()
        html = t.render(c)
        return render_to_response('codevaldapp/template_form.html', {"title": "CodeVald : Convert SQL", "action": "codevaldapp:MySQLToXML", "pagetitle": "Generate XML", "pagesubtitle": "MySQL to XML", "CurrPage": "Generate XML", "menu": menu, "content": html}, context_instance=RequestContext(request))


def GenerateCode(request):
    menu = GetMenu("codevaldapp:GenerateCode")
    messageclass = "msgsuccess"
    if request.method == "POST":
        message = ""
        try:
            XML = request.POST['txtXML']
            CodeTemplate = request.POST['txtCodeTemplate']
        except:
            XML = ""
            CodeTemplate = ""

        if XML != "" and CodeTemplate != "":
            o_XML = ReadXML.ReadXML(XML)
            o_template = CodeTemplate

            o_GenerateCode = CodeGenerator.GenerateCode(o_template)
            pycodegenerator = o_GenerateCode.pycodegenerator
            codelist = []

            #strPath = os.path.dirname(__file__)+"/../data/"
            #filename = 'codevaldapp/data/codetorun11.txt'
            #f = open(filename, "w")
            #f.write(pycodegenerator)
            #f.close()

            code = ""
            #pycodegenerator = open('codevaldapp/data/codetorun.txt', 'r+')
            #pycodegenerator = pycodegenerator.read()

            exec(pycodegenerator.replace('\r', ''))
            for each_code in codelist:
                code = code + each_code
            messageclass = "msgsuccess"
            message = "Process Complete!"

        content = open('codevaldapp/static/codevaldapp/assets/content/GenerateCode.html', 'r+')
        t = Template(content.read())
        c = Context({"activetab": "Code", "XML": XML, "CodeTemplate": CodeTemplate, "NewCode": code, "message": message, "messageclass": messageclass})
        content.close()
        html = t.render(c)

        return render_to_response('codevaldapp/template_form.html', {"title": "CodeVald : GenerateCode", "action": "codevaldapp:GenerateCode", "pagetitle": "Generate Code", "pagesubtitle": "XML + Template = (formative) Code", "CurrPage": "Generate Code", "menu": menu, "content": html}, context_instance=RequestContext(request))
    else:
        content = open('codevaldapp/static/codevaldapp/assets/content/GenerateCode.html', 'r+')
        sampleXML = open('codevaldapp/data/samplexml.xml', 'r+')
        sampleXML = sampleXML.read()
        sampleXML = sampleXML.__str__()

        sampleTemplate = open('codevaldapp/data/sampletemplate.txt', 'r+')
        sampleTemplate = sampleTemplate.read()
        sampleTemplate = sampleTemplate.__str__()

        t = Template(content.read())
        c = Context({"activetab": "XML", "XML": sampleXML, "CodeTemplate": sampleTemplate, 'NewCode': ""})
        content.close()
        html = t.render(c)
        return render_to_response('codevaldapp/template_form.html', {"title": "CodeVald : GenerateCode", "action": "codevaldapp:GenerateCode", "pagetitle": "Generate Code", "pagesubtitle": "XML + Template = (formative) Code", "CurrPage": "Generate Code", "menu": menu, "content": html}, context_instance=RequestContext(request))

