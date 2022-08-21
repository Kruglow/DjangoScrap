from django.urls import path

from scrap.views import home_view, Search, VList

urlpatterns = [
    path('', home_view,name='home'),
    path('list', VList.as_view(), name='list')
]