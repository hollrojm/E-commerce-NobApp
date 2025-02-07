from core.models import Category, Vendor, Product, CartOrder, CartOrderItems, ProductImages, Wishlist, ProductReview,Address

def categories(request):
    categories = Category.objects.filter(category_status='Published')
    address = Address.objects.get(user= request.user)
    return {
        "categories":categories,
        "address":address,
    }