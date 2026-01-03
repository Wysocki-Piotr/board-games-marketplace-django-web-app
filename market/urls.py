from django.urls import path, reverse_lazy
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
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='market/password_reset_form.html',
            success_url=reverse_lazy('market:password_reset_done')
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='market/password_reset_done.html'
         ),
         name='password_reset_done'),
]
