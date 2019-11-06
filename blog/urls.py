from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('dashboard/', views.dashboard, name='blog-dashboard'),
    path('results/', views.results, name='department-results'),
    path('upload/', views.upload_files, name='uploadFiles'),
    path('files/', views.files, name='files')
]
