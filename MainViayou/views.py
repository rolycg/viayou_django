from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.utils import translation
import requests


# Create your views here.


def home(request):
    try:
        lang = request.session[translation.LANGUAGE_SESSION_KEY]
    except KeyError:
        translation.activate('en')
        request.session[translation.LANGUAGE_SESSION_KEY] = 'en'
    return render(request, 'home.html', {
        'hola': 'Hola mUndo'

    })


def get_cities():
    res = requests.get('http://restcountries.eu/rest/')
    print(res)


def change_language(request):
    if request.method == 'GET':
        try:
            lang = request.GET['lang']
        except KeyError:
            raise Http404()
        try:
            ret = HttpResponseRedirect(request.environ['HTTP_REFERER'].split('?')[0])
        except KeyError:
            ret = HttpResponseRedirect('/')
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
        return ret
    else:
        raise Http404()
