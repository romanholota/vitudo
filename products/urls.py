from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('<int:product_id>/',views.detail, name='detail'),
    path('<int:product_id>/items/',views.items, name='items'),
]
