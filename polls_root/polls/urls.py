from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', view=views.index, name='index'),
    path('questions/<int:pk>', view=views.detail, name='detail'),
    path('questions/<int:pk>/vote', view=views.vote, name='vote'),
    path('questions/<int:pk>/vote-own', view=views.vote_own, name='vote-own'),
    path('questions/<int:pk>/results', view=views.results, name='results')
]
