from django.http import HttpResponse
from django.shortcuts import render
from core.models import Category, Vendor, Product, CartOrder, CartOrderItems, ProductImages, Wishlist, ProductReview,Address


def index(request):
    products = Product.objects.all().order_by("-id")

    context ={
        "products":products
    }
    return render(request, 'core/index.html', context)
