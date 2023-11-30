from django.urls import path
from . import views

app_name = 'gpt'

urlpatterns = [
    path('', views.main, name='main'),
    path('sites/', views.site_selection, name='site_selection'),
    path('process_selection/', views.process_selection, name='process_selection'),
    path('confirmation/', views.process_selection, name='confirmation'),
    path('get-log-data/', views.get_log_data, name='get_log_data')
]
