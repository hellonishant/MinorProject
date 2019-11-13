from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('login/', views.login_view, name='blog-login'),
    path('logout/', views.logout_view, name='blog-logout'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('dashboard/', views.dashboard, name='blog-dashboard'),
    path('results/<str:dep>/<int:sem>/<str:section>/', views.results, name='department-results'),
    path('result/', views.result_search, name='student-result-search'),
    path('result/<str:roll_no>/', views.result, name='student-result'),
    path('upload/', views.upload_files, name='uploadFiles'),
    path('files/', views.files, name='files'),
    path('download/<int:pk>/', views.download, name='download'),
    path('delete/<int:pk>/', views.delete, name='delete'),
]
