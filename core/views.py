from django.http import HttpResponse
from django.shortcuts import render
from core.models import Category, Vendor, Product, CartOrder, CartOrderItems, ProductImages, Wishlist, ProductReview,Address


def index(request):

    try:
        products = Product.objects.filter(product_status='Published', featured=True)
        
        context ={
            "products":products,
            
        }
        return render(request, 'core/index.html', context)

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

def product_list_view(request):

    try:
        products = Product.objects.filter(product_status='Published')
        
        context ={
            "products":products,
            
        }
        return render(request, 'core/product-list.html', context)

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
    
def category_list_view(request):

    try:
        categories = Category.objects.filter(category_status='Published')
        
        context ={
            "categories":categories,
            
        }
        return render(request, 'core/category-list.html', context)

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

def product_list_category_view(request,cid):

        try:
            category = Category.objects.get(cid=cid)
            products = Product.objects.filter(product_status='Published', category_id=category)
            context ={
                "category":category,
                "products":products,
            }
            return render(request, 'core/category-product-list.html', context)
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)
            

def vendor_list_view(request):

    try:
        vendors = Vendor.objects.filter(vendor_status='Published')
        
        context ={
            "vendors":vendors,
            
        }
        return render(request, 'core/vendor-list.html', context)

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)