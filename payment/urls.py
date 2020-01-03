from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls.static import static



app_name = 'payment'


urlpatterns = [

    path('users',views.UsersList.as_view()),
    path('register', views.Register.as_view()),
    path('login', views.UserValidView.as_view()),
    path('users/<int:pk>/',views.UserDetails.as_view()),
    path('<int:pk>/product',views.ProductView.as_view()),
    path('users/<int:pk>/cart',views.CartView.as_view()),
    path('send',views.sendmail.as_view()),
    path('paid',views.successredirect.as_view()),
    path('users/<int:pk>/po',views.Orders.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

] 
