from django.urls import path
from .views import index, showActivity, postActivity

app_name = 'activity'
urlpatterns = [
    path('', index),
    path('postActivity/', postActivity),
    path('showActivity/', showActivity),
]