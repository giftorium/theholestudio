from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productions/', views.productions, name='productions'),
    path('productions/<slug:slug>/', views.production_detail, name='production_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
