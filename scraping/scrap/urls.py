from django.urls import path

from scrap.views import Home

urlpatterns = [
    path('', Home.as_view())
]