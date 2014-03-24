from django.shortcuts import render
from django.shortcuts import render_to_response
from django.templatetags.static import static
from django.template import Template, Context, RequestContext, loader
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from codevald_generators import MySQLtoXML

def IndexView(request):
    content = open('codevaldapp/' + static('codevaldapp/content/home.html'), 'r+')
    t = Template(content.read())
    content.close()
    html = t.render(Context({'router_map'}))

    return render(request, 'codevaldapp/template.html', {"title": "CodeVald : Home", "pagetitle": "CodeVald", "pagesubtitle": "XML + Template = (principal) Code", "content": html})


def XMLToCode(request):
    content = open('codevaldapp/' + static('codevaldapp/content/XMLToCode.html'), 'r+')
    t = Template(content.read())
    content.close()
    html = t.render(Context({'router_map'}))

    return render(request, 'codevaldapp/template.html', {"title": "CodeVald : XMLToCode", "pagetitle": "Convert", "pagesubtitle": "XML + Template = (principal) Code", "CurrPage": "XML to Code", "content": html})


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

        return render_to_response('codevaldapp/template_form.html', {'content': html}, context_instance=RequestContext(request))
    else:
        content = open('codevaldapp/' + static('codevaldapp/content/MySQLToXML.html'), 'r+')
        t = Template(content.read())
        c = Context({"MySQL": "oi", "XML": "oi2"})
        content.close()
        html = t.render(c)
        return render_to_response('codevaldapp/template_form.html', {'content': html}, context_instance=RequestContext(request))