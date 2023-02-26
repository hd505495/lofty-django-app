from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('keys/list/', views.keyvalue_list),
    path('keys/', views.keyvalue_create),
    path('keys/<str:key>/increment/', views.keyvalue_increment),

    path('dogs/generate', views.dogs_generate),
    path('dog/', views.dog_get),
]