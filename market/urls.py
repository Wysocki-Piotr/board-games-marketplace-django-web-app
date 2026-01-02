from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
]