from django.urls import path
from .views.register import RegisterView 
from .views.login import PheonixLoginView,PheonixLogout  
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',PheonixLoginView.as_view(),name='login'),
    path('logout/',PheonixLogout.as_view(),name='logout')
    
]
