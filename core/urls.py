from django.urls import path
from .views import index
from core import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('product/', views.product_list_view, name='product-list'),
    path('category/', views.category_list_view, name='category-list'),
]