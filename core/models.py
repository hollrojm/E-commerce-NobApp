from django.db import models

from django.db import models
from shortuuidfield import ShortUUIDField
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('active', 'activo', 'Active','Activo'),
    ('inactive', 'inactivo', 'Inactive','Inactivo'),
    ('processing', 'procesando', 'Processing','Procesando'),
    ('delivered', 'entregado', 'Delivered','Entregado'),
)

STATUS = (
    ('draft', 'borrador', 'Draft','Borrador'),
    ('disabled', 'deshabilitado', 'Disabled','Deshabilitado'),
    ('rejected', 'rechazado', 'Rejected','Rechazado'),
    ('approved', 'aprobado', 'Approved','Aprobado'),
    ('pending', 'pendiente', 'Pending','Pendiente'),
    ('published', 'publicado', 'Published','Publicado'),
    ('unpublished', 'no publicado', 'Unpublished','No publicado'),
    ('in_review', 'en_revisión', 'In_Review','En_Revisión'),
)
RATING = (
    ('1', '★☆☆☆☆'),
    ('2', '★★☆☆☆'),
    ('3', '★★★☆☆'),
    ('4', '★★★★☆'),
    ('5', '★★★★★'),
)

def user_directory_path(instance, filename):
    return f'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat_', alphabet='abcdefgh12345')
    title = models.CharField(_('titulo'))(max_length=100, default='Título de la categoría')
    image = models.ImageField(_('imagen_categoria'))(upload_to='category', default='category.jpg')
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

class Tags(models.Model):
    pass

    class Meta:
        verbose_name = _('etiqueta')
        verbose_name_plural = _('etiquetas')

    def __str__(self):
        return self.title

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven_', alphabet='abcdefgh12345')
    vendor_name = models.CharField(_('nombre_proveedor'))(max_length=100, default='Nombre del proveedor')
    logo = models.ImageField(_('logo'))(upload_to=user_directory_path, default='proveedor.jpg')
    description = models.TextField(_('descripción'))(null=True, blank=True, default='Descripción del proveedor')
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
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='pro_', alphabet='abcdefgh12345')
    product_title = models.CharField(_('titulo_producto'))(max_length=100, default='Título del producto')
    image = models.ImageField(_('imagen_producto'))(upload_to=user_directory_path , default='product.jpg')
    description = models.TextField(_('descripción'))(max_length=255, default='Descripción del producto')
    price = models.DecimalField(_('precio'), max_digits=10, decimal_places=2, default=1.99)
    old_price = models.DecimalField(_('precio_anterior'), max_digits=10, decimal_places=2, default=2.99)
    specifications = models.TextField(_('especificaciones'))(null=True, blank=True)
    tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    in_stock = models.BooleanField(_('en_stock'), default=True)
    stock = models.IntegerField(_('stock'))
    product_status = models.CharField(choices=STATUS, default='en_revisión', max_length=20)
    status = models.BooleanField(_('estado'), default=True)
    featured = models.BooleanField(_('destacado'), default=False)
    rating = models.CharField(choices=RATING, default='★★★☆☆', max_length=5)
    sku = ShortUUIDField(unique=True, length=4, max_length=20, prefix='sku_', alphabet='1234567890')
    digital = models.BooleanField(_('digital'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('producto')
        verbose_name_plural = _('productos')

    def product_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')

    def __str__(self):
        return self.product_title

    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    
    def get_percentage_discount(self):
        return (self.old_price - self.price) / self.old_price * 100
    

class ProductImages(models.Model):
    image = models.ImageField(_('imagen_producto'))(upload_to='product-images', default='product.jpg')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('imagen_producto')
        verbose_name_plural = _('imagenes_productos')

    
