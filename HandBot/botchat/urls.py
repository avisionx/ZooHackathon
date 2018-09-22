from django.urls import path
from .views import *

app_name = 'botchat'
urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='authPage'),
    path('api/', api.as_view(), name='api'),
]