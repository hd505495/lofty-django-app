from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('keys/list/', views.KeyValueList.as_view()),
    path('keys/:id/', views.KeyValueCreate.as_view()),
    path('keys/:id/increment/', views.KeyValueIncrement.as_view())
]