from django.urls import path

from scrap.views import VList, Search

urlpatterns = [
    path('', VList.as_view(),name='list'),
    path('search', Search.as_view())
]