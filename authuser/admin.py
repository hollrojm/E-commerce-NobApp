from django.contrib import admin

from authuser.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'colored_name', 'phone_number', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'profile_picture']
    search_fields = ('email', 'name', 'last_name', 'phone_number')
    list_filter = ('is_superuser', 'is_staff', 'is_active')

admin.site.register(User, UserAdmin)
