from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('signup', views.SignUpVS, basename='signup')
router.register('login', views.LogIn, basename='login')


urlpatterns =[
    path('', include(router.urls)),
]