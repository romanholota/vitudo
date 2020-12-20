from django.urls import path, re_path

from . import views

app_name = 'items'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('<int:item_id>/', views.detail, name='detail'),
    path('<int:item_id>/transfers/', views.transfers, name='transfers'),
    path('<int:item_id>/gallery/', views.edit_gallery, name='edit_gallery'),
    path('<int:item_id>/gallery/add/', views.image_add, name='image_add'),
]
