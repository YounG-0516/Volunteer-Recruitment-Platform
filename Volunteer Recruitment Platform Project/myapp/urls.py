from django.urls import path
from .views import show_activity, apply, submit_application, register, login, check, approve, reject, editActivity, deleteActivity

app_name = 'myapp'
urlpatterns = [
    path('showActivity/', show_activity, name='show_activity'),
    path('apply/', apply, name='apply'),
    path('register/', register),
    path('login/', login),
    path('check/', check),
    path('submit/<slug:activity_id>', submit_application, name='submit_application'),
    path('approve/<slug:application_id>', approve, name='approve_application'),
    path('reject/<slug:application_id>', reject, name='reject_application'),
    path('editActivity/', editActivity, name='edit_activity'),
    path('deleteActivity/<slug:activity_id>', deleteActivity, name='delete_activity'),
]