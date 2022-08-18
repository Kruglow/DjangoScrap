from django.shortcuts import render
from django.views.generic import ListView

from scrap.models import Vacancy


class Home(ListView):
    model = Vacancy
    template_name = 'skrap/home.html'
    context_object_name = 'vacancy'

