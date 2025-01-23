from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.files.storage import default_storage
import uuid
import os
from django.utils.html import mark_safe
from django.contrib import admin
from django.utils.html import format_html

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('El Email es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser debe tener is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

def profile_picture_path(instance, filename):
    random_filename = str(uuid.uuid4())
    extension = os.path.splitext(filename)[1]
    return 'users/{}/{}{}'.format(instance.user.username, random_filename, extension)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('dirección email'), unique=True)
    name = models.CharField(_('nombre'), max_length=255, blank=True)
    last_name = models.CharField(_('apellido'), max_length=255, blank=True)
    username = models.CharField(_('nombre de usuario'), max_length=255, blank=True,default='default.png')
    phone_number = models.CharField(_('número de teléfono'), max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = CustomUserManager()
    
    
    

    @admin.display
    def full_name(self):
        return format_html(
            '<span >{} {}</span>',
            self.name,
            self.last_name,
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def save(self, *args, **kwargs):
        if self.pk and self.profile_picture.name != 'default.png':
            old_profile = User.objects.get(pk=self.pk)
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'default.png')

            if old_profile.profile_picture.path != self.profile_picture.path and old_profile.profile_picture.path != default_image_path:
                default_storage.delete(old_profile.profile_picture.path)
        
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

    def profile_image(self):
        if self.profile_picture:
            return mark_safe(f'<img src="{self.profile_picture.url}" width="50" height="50" />')
        return mark_safe('<img src="/path/to/default/image.png" width="50" height="50" />')

    def __str__(self):
        return self.email

