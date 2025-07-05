# productos/models.py

from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    """
    Modelo para representar un producto en la ferretería FerrRokect.
    """
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Nombre del Producto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción detallada")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    stock = models.IntegerField(default=0, verbose_name="Cantidad en Stock")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Imagen del Producto") # <<-- ¡Añade esta línea!
    codigo_sku = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Código SKU")
    categoria = models.CharField(max_length=100, blank=True, null=True, verbose_name="Categoría")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    ultima_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    activo = models.BooleanField(default=True, verbose_name="Producto Activo")

    class Meta:
        verbose_name = "Producto de Ferretería"
        verbose_name_plural = "Productos de Ferretería"
        ordering = ['nombre'] # Ordenar productos por nombre por defecto

    def __str__(self):
        """
        Devuelve una representación en cadena del objeto Producto.
        """
        return self.nombre
        
class Cart(models.Model):
    """
    Modelo para el carrito de compras de un usuario.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    # Un carrito puede pertenecer a un usuario registrado (OneToOne)
    # o ser anónimo (null=True, blank=True) para usuarios no logueados.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Carrito de Compras"
        verbose_name_plural = "Carritos de Compras"

    def __str__(self):
        if self.user:
            return f"Carrito de {self.user.username}"
        return f"Carrito Anónimo ({self.id})"

class CartItem(models.Model):
    """
    Modelo para los ítems dentro de un carrito de compras.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Ítem del Carrito"
        verbose_name_plural = "Ítems del Carrito"
        unique_together = ('cart', 'producto') # Un producto solo puede estar una vez en el mismo carrito

    def __str__(self):
        return f"{self.quantity} x {self.producto.nombre} en carrito {self.cart.id}"

    @property
    def total_price(self):
        return self.quantity * self.producto.precio