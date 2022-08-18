from django.shortcuts import render
from django.views.generic import ListView

from scrap.forms import SearchForm
from scrap.models import Vacancy, City


class Home(ListView):
    model = Vacancy
    template_name = 'skrap/home.html'
    context_object_name = 'vacancy'

class Search(ListView):
    model = Vacancy
    fields = ['city',]
    template_name = 'skrap/search.html'