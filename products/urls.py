from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('<int:product_id>/',views.detail, name='detail'),
    path('<int:product_id>/items/',views.items, name='items'),
    path('brands/', views.brands, name='brands'),
    path('brands/add/', views.brand_add, name='brand_add'),
    path('brands/<int:brand_id>/', views.brand_detail, name='brand_detail'),
    path('brands/<int:brand_id>/products/', views.brand_products, name='brand_products'),
    path('brands/<int:brand_id>/remove/', views.brand_remove, name='brand_remove'),
]
