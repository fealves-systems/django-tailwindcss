from django.urls import path
from accounts import views as views

urlpatterns = [
    path('login/', views.accounts_login, name='login'),
    path('logout/', views.accounts_logout, name='logout'),
    path('register/', views.accounts_register, name='register'),
    path('forgot_password/', views.accounts_forgot_password, name='forgot_password'),
    
    path('password_reset/', views.accounts_password_reset.as_view(), name='password_reset'),
    path('password_reset_done/', views.accounts_password_reset_done.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.accounts_password_reset_confirm.as_view(), name='password_reset_confirm'),
    path('password_reset_completed/', views.accounts_password_reset_complete.as_view(), name='password_reset_complete'),

]