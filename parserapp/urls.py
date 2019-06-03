from django.urls import path
from parserapp.views import ParserView

urlpatterns = [
    path('', ParserView.as_view(), name='parserview'),
]