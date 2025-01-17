from django.db import models

from django.db import models
from shortuuidfield import ShortUUIDField
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return f'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat_', alphabet='abcdefgh12345')
    title = models.CharField(_('titulo'))(max_length=100)
    image = models.ImageField(_('imagen_categoria'))(upload_to='category')
    description = models.TextField(_('descripción'))()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('categoria')
        verbose_name_plural = _('categorias')

    def category_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')

    def __str__(self):
        return self.title

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven_', alphabet='abcdefgh12345')
    vendor_name = models.CharField(_('nombre_proveedor'))(max_length=100)
    logo = models.ImageField(_('logo'))(upload_to=user_directory_path)
    description = models.TextField(_('descripción'))(null=True, blank=True)
    address = models.CharField(_('dirección'))(max_length=255, default='Calle 6 sur # 71d - 77')
    contact = models.CharField(_('contacto'))(max_length=100, default='+57 (123) 4567890')
    chat_resp_time = models.CharField(_('tiempo de respuesta'))(max_length=100, default='En menos de 24 horas')
    shipping_time = models.CharField(_('tiempo de envío'))(max_length=100, default='De 3 a 5 días hábiles')
    shipping_policy = models.TextField(_('política de envío'))(null=True, blank=True)
    authentic_rating = models.FloatField(_('calificación auténtica'))(default=4.5)
    days_return = models.IntegerField(_('días de devolución'))(default=30)
    warranty = models.CharField(_('garantía'))(max_length=100, default='Garantía de 6 meses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_vendor_name = _('proveedor')
        verbose_vendor_name_plural = _('proveedores')

    def vendor_logo(self):
        return mark_safe(f'<img src="{self.logo.url}" width="100" height="100" />')

    def __str__(self):
        return self.vendor_name
