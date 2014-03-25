from django.shortcuts import render
from django.shortcuts import render_to_response
from django.templatetags.static import static
from django.template import Template, Context, RequestContext
from codevald_generators import MySQLtoXML
from codevald_generators import ReadXML
from codevald_generators import CodeGenerator


def IndexView(request):
    content = open('codevaldapp/' + static('codevaldapp/content/home.html'), 'r+')
    t = Template(content.read())
    content.close()
    html = t.render(Context({'router_map'}))

    return render(request, 'codevaldapp/template.html', {"title": "CodeVald : Home", "pagetitle": "CodeVald", "pagesubtitle": "XML + Template = (formative) Code", "content": html})


def Team(request):
    content = open('codevaldapp/' + static('codevaldapp/content/team.html'), 'r+')
    t = Template(content.read())
    content.close()
    html = t.render(Context({'router_map'}))

    return render(request, 'codevaldapp/template.html', {"title": "CodeVald : Team", "pagetitle": "Team", "pagesubtitle": "", "CurrPage": "Team", "content": html})


def ConvertMySQLToXML(request):
    if request.method == "POST":
        try:
            MySQL = request.POST['txtMySQL']
        except:
            MySQL = ""
            XML = ""

        if MySQL != "":
            NewXML = MySQLtoXML.MySQLtoXML(MySQL)
            XML = NewXML.GetXML

        content = open('codevaldapp/' + static('codevaldapp/content/MySQLToXML.html'), 'r+')
        t = Template(content.read())
        c = Context({"MySQL": MySQL, "XML": XML})
        content.close()
        html = t.render(c)

        return render_to_response('codevaldapp/template_form.html', {"title": "CodeVald : Convert SQL", "action": "codevaldapp:ConvertMySQLToXML", "pagetitle": "Generate XML", "pagesubtitle": "MySQL to XML", "CurrPage": "Generate XML", "content": html}, context_instance=RequestContext(request))
    else:
        content = open('codevaldapp/' + static('codevaldapp/content/MySQLToXML.html'), 'r+')
        t = Template(content.read())
        c = Context({"MySQL": "", "XML": ""})
        content.close()
        html = t.render(c)
        return render_to_response('codevaldapp/template_form.html', {"title": "CodeVald : Convert SQL", "action": "codevaldapp:ConvertMySQLToXML", "pagetitle": "Generate XML", "pagesubtitle": "MySQL to XML", "CurrPage": "Generate XML", "content": html}, context_instance=RequestContext(request))


def GenerateCode(request):
    if request.method == "POST":
        try:
            XML = request.POST['txtXML']
            CodeTemplate = request.POST['txtCodeTemplate']
        except:
            XML = ""
            CodeTemplate = ""

        if XML != "" and CodeTemplate != "":
            o_ReadXML = ReadXML.ReadXML(XML)
            o_template = CodeTemplate

            o_GenerateCode = CodeGenerator.GenerateCode(o_template)
            pycodegenerator = o_GenerateCode.pycodegenerator
            codelist = []
            exec(pycodegenerator)
            code = ""
            for each_code in codelist:
                code = code + each_code

        content = open('codevaldapp/' + static('codevaldapp/content/GenerateCode.html'), 'r+')
        t = Template(content.read())
        c = Context({"XML": XML, "CodeTemplate": CodeTemplate, "NewCode": code})
        content.close()
        html = t.render(c)

        return render_to_response('codevaldapp/template_form.html', {"title": "CodeVald : GenerateCode", "action": "codevaldapp:GenerateCode", "pagetitle": "Generate Code", "pagesubtitle": "XML + Template = (formative) Code", "CurrPage": "Generate Code", "content": html}, context_instance=RequestContext(request))
    else:
        content = open('codevaldapp/' + static('codevaldapp/content/GenerateCode.html'), 'r+')
        t = Template(content.read())
        c = Context({"XML": "", "CodeTemplate": "", 'NewCode': ""})
        content.close()
        html = t.render(c)
        return render_to_response('codevaldapp/template_form.html', {"title": "CodeVald : GenerateCode", "action": "codevaldapp:GenerateCode", "pagetitle": "Generate Code", "pagesubtitle": "XML + Template = (formative) Code", "CurrPage": "Generate Code", "content": html}, context_instance=RequestContext(request))