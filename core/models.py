from django.db import models

from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS_CHOICES = (
    ('Active', _('Activo') ),
    ('Inactive',_('Inactivo')),
    ('Processing', _('Procesando')),
    ('Delivered',_('Entregado')),
)

STATUS = (
    
    ( 'Draft',_('Borrador')),
    ( 'Disabled',_('Deshabilitado')),
    ( 'Rejected',_('Rechazado')),
    ( 'Approved',_('Aprobado')),
    ( 'Pending',_('Pendiente')),
    ( 'Published',_('Publicado')),
    ( 'Unpublished',_('No publicado')),
    ( 'InReview',_('En Revisión')),
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
    title = models.CharField(_('titulo'), max_length=100, default='Título de la categoría')
    image = models.ImageField(_('imagen_categoria'), upload_to='category', default='category.jpg')
    description = models.TextField(_('descripción'))
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
    vendor_name = models.CharField(_('Empresa'),max_length=100, default='Nombre del proveedor')
    logo = models.ImageField(_('logo'),upload_to=user_directory_path, default='proveedor.jpg')
    description = models.TextField(_('descripción'),null=True, blank=True, default='Descripción del proveedor')
    address = models.CharField(_('dirección'),max_length=255, default='Calle 6 sur # 71d - 77')
    contact = models.CharField(_('contacto'),max_length=100, default='+57 (123) 4567890')
    chat_resp_time = models.CharField(_('tiempo de respuesta'),max_length=100, default='En menos de 24 horas')
    shipping_time = models.CharField(_('tiempo de envío'),max_length=100, default='De 3 a 5 días hábiles')
    shipping_policy = models.TextField(_('política de envío'),null=True, blank=True)
    authentic_rating = models.FloatField(_('calificación auténtica'),default=4.5)
    days_return = models.IntegerField(_('días de devolución'),default=30)
    warranty = models.CharField(_('garantía'),max_length=100, default='Garantía de 6 meses')
    website = models.URLField(_('sitio_web'),max_length=100, default='https://www.example.com')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('proveedor')
        verbose_name_plural = _('proveedores')

    def vendor_logo(self):
        return mark_safe(f'<img src="{self.logo.url}" width="100" height="100" />')

    def __str__(self):
        return self.vendor_name
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='pro_', alphabet='abcdefgh12345')
    product_title = models.CharField(_('Titulo Producto'),max_length=100, default='Título del producto')
    image = models.ImageField(_('Imagen'),upload_to=user_directory_path , default='product.jpg')
    description = models.TextField(_('Descripción'),max_length=255, default='Descripción del producto')
    price = models.DecimalField(_('Precio'), max_digits=10, decimal_places=2, default=1.99)
    old_price = models.DecimalField(_('Precio Anterior'), max_digits=10, decimal_places=2, default=2.99)
    specifications = models.TextField(_('Especificaciones'),null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    #tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    in_stock = models.BooleanField(_('En Stock'), default=True)
    stock = models.IntegerField(_('stock'))
    product_status = models.CharField(choices=STATUS, default='En revisión', max_length=20)
    status = models.BooleanField(_('Estado'), default=True)
    featured = models.BooleanField(_('Destacado'), default=False)
    sku = ShortUUIDField(unique=True, length=4, max_length=20, prefix='sku_', alphabet='1234567890')
    digital = models.BooleanField(_('Digital'), default=False)
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
    image = models.ImageField(_('imagen_producto'),upload_to='product-images', default='product.jpg')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('imagen_producto')
        verbose_name_plural = _('imagenes_productos')

  ##############################Cart  Order, OrderItems, and address############################################

    
class CartOrder(models.Model):
    cid = ShortUUIDField(unique=True, length=4, max_length=20, prefix='cart_', alphabet='abcdefgh12345')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(_('precio'), max_digits=10, decimal_places=2, default=1.99)
    paid_status= models.BooleanField(_('pago_seguimiento'), default=False)
    product_status = models.CharField(choices=STATUS_CHOICES, default='Procesando', max_length=30)
    order_date = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = _('pedido_carrito')
        verbose_name_plural = _('pedidos_carrito')

    
   
   
   
class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoce_number = models.CharField(_('número_factura'),max_length=200, default='Número de factura')
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(_('precio'), max_digits=10, decimal_places=2, default=1.99)
    total = models.DecimalField(_('total'), max_digits=10, decimal_places=2, default=1.99)

    class Meta:
        verbose_name = _('pedido_carrito_item')
        verbose_name_plural = _('pedidos_carrito_items')

    def order_image(self):
        return mark_safe(f'<img src="/media/{self.image}" width="50" height="50" />')

   
  ##############################Product Review, wishlist, address############################################

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(choices=RATING, default='★★★☆☆', max_length=None)
    review = models.TextField(_('revisión'),)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('revisión_producto')
        verbose_name_plural = _('revisiones_producto')

    def __str__(self):
        return self.product.product_title
    
    def get_rating(self):
        return self.rating

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('lista_deseos')
        verbose_name_plural = _('listas_deseos')

    def __str__(self):
        return self.product.product_title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(_('dirección'),max_length=255, null=True, blank=True)
    status = models.BooleanField(_('estado'), default=False)
    city = models.CharField(_('ciudad'),max_length=100, null=True, blank=True)
    state = models.CharField(_('estado'),max_length=100,null=True, blank=True)
    country = models.CharField(_('país'),max_length=100, null=True, blank=True)
    zip_code = models.CharField(_('código postal'),max_length=10,null=True, blank=True)
    phone = models.CharField(_('teléfono'),max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('dirección')
        verbose_name_plural = _('direcciones')
    


