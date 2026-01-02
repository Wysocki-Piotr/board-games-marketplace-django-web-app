from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'market'

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('register/', views.register, name='register'),
    path('add/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/kup/', views.kup_gre, name='buy_listing'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]