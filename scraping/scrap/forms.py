from django import forms

from scrap.models import City, Language, Vacancy


class SearchForm(forms.ModelForm):
   class Meta:
      model = Vacancy
      fields = ("city",)