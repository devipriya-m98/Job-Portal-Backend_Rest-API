from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('jobs/', views.job_list),
    path('jobs/<int:pk>/', views.job_detail),
    path('candidate-profile/', views.candidate_profile),
    path('jobs/<int:pk>/apply/', views.job_apply),
    path('applications/', views.application_list),
    path('applications/<int:pk>/', views.application_detail),
    path('applications/<int:pk>/status', views.application_status),


]