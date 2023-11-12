from django.urls import path

from .views import register, login, show_info, logout, applyResult

app_name = 'account'
urlpatterns = [
    path('register/', register, name='register'),
    path('information/', show_info, name='show_info'),
    path('applyResult/', applyResult, name='applyResult'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]