"""
URL configuration for ferrrokect_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# ferrrokect_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importaciones de vistas de tu aplicación 'productos'
from productos.views import (
    home_ferreteria,
    about_us,
    productos_list,
    add_to_cart,
    cart_detail,
    remove_from_cart,
    update_cart_item,
    checkout 
)

# Importación de vistas de tu proyecto principal (si tienes alguna aquí)
from ferrrokect_project.views import register # Asumiendo que 'register' está aquí

urlpatterns = [
    # URLs de administración de Django
    path('admin/', admin.site.urls),

    # Incluir URLs de tu aplicación 'productos' para la API REST
    path('api/', include('productos.urls')),

    # URLs de autenticación de Django
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register, name='register'),

    # URLs de tus páginas principales
    path('', home_ferreteria, name='home'),
    path('sobre-nosotros/', about_us, name='about_us'),
    path('productos/', productos_list, name='productos_list'),

    # URLs para el carrito de compras
    path('add-to-cart/<int:producto_id>/', add_to_cart, name='add_to_cart'),
    path('carrito/', cart_detail, name='cart_detail'),
    path('carrito/eliminar/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('carrito/actualizar/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('checkout/', checkout, name='checkout'),
]

# Configuración para servir archivos multimedia durante el desarrollo
# Esto solo debe usarse en modo DEBUG (desarrollo), no en producción.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)