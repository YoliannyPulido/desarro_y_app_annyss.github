# productos/admin.py

from django.contrib import admin
from .models import Producto, Cart, CartItem # <<-- ¡Importa los nuevos modelos!

admin.site.register(Producto)
admin.site.register(Cart) # <<-- ¡Registra el modelo Cart!
admin.site.register(CartItem) # <<-- ¡Registra el modelo CartItem!