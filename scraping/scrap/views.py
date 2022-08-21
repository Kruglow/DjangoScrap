from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView

from scrap.forms import FindForm
from scrap.models import Vacancy, City


# class Home(ListView):
#     model = Vacancy
#     template_name = 'skrap/home.html'
#     context_object_name = 'vacancy'

def home_view(request):
    # print(request.GET)
    form = FindForm()

    return render(request, 'skrap/home.html', {'form': form})


class VList(ListView):
    model = Vacancy
    template_name = 'skrap/list.html'
    form = FindForm()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form

        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        qs = []
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            qs = Vacancy.objects.filter(**_filter).select_related('city', 'language')
        return qs


class Search(ListView):
    model = Vacancy
    fields = ['city',]
    template_name = 'skrap/search.html'