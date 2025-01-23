from django.contrib import admin
from authuser.models import User
from django.utils.html import mark_safe


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'username', 'phone_number', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'profile_image']
    search_fields = ('email', 'name', 'last_name', 'phone_number')
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    
    def profile_picture_thumbnail(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" width="50" height="50" style="border-radius: 50%;" />')
        return 'No Image'
    
    profile_picture_thumbnail.short_description = 'Profile Picture'

admin.site.register(User, UserAdmin)



