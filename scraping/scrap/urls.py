from django.urls import path

from scrap.views import Home, Search

urlpatterns = [
    path('', Home.as_view()),
    path('search', Search.as_view())
]