from django.urls import path
from .views import index
from core import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    
    path('products/', views.product_list_view, name='product-list'),
    path('product/<pid>/', views.product_detail_view, name='product-detail'),
    
    path('categories/', views.category_list_view, name='category-list'),
    path('category/<cid>/', views.product_list_category_view, name='category-product-list'),
    
    path('vendors/', views.vendor_list_view, name='vendor-list'),
    path('vendor/<vid>/', views.vendor_detail_view, name='vendor-detail'),
    
    
]