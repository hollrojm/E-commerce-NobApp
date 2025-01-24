from core.models import Category, Vendor, Product, CartOrder, CartOrderItems, ProductImages, Wishlist, ProductReview,Address

def categories(request):
    categories = Category.objects.filter(category_status='Published')
    return {
        "categories":categories
    }