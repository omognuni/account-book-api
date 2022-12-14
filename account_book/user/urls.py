from django.urls import path

from user import views

# app name for reverse mapping
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
