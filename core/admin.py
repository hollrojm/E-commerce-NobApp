from django.contrib import admin
from core.models import Category, Vendor, Product, CartOrder, CartOrderItems, ProductImages, Wishlist, ProductReview,Address

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user','product_title', 'product_image', 'price','featured','product_status', 'stock', 'created_at']
    list_per_page = 10

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','category_image' ]
    list_per_page = 10

class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_name','vendor_logo' ]
    list_per_page = 10

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price','paid_status','product_status', 'order_date']
    list_per_page = 10

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoce_number', 'item', 'quantity','image', 'price','total']
    list_per_page = 10

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product',  'rating', 'review', 'rating']    
    list_per_page = 10

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']    
    list_per_page = 10

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'city', 'state', 'phone', 'country', 'status']    
    list_per_page = 10

admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductImages)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.site_header = 'Artoys Ecommerce Admin'
