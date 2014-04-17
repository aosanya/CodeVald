from django.shortcuts import render
from django.template import Template, Context
from inspect import stack, getmodule


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

