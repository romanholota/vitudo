from django.urls import path

from . import views

app_name = 'transfers'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.transfer, name='transfer'),
    path('<int:item_id>/', views.transfer_item, name='transfer_item'),
    path('new/create/', views.create_transfer, name='create_transfer'),
    path('locations/', views.get_locations, name='get_locations'),
    path('return/item/<int:item_id>/', views.return_item, name='return_item'),
]