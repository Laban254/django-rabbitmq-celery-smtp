from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home_view, name='home'), 
    path('', views.send_message, name='send_message'),
    path('logs/', views.view_log_file, name='view_log_file'),
]