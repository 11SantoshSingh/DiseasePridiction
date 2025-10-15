from django.urls import path
from . import views

urlpatterns = [
    # ...existing url patterns...
    path('history', views.history, name='history'),
    path('pridiction', views.pridiction, name='pridiction'),
    # ...existing url patterns...
]