# productos/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required # Esta importación es útil, aunque no la uses en todas las vistas de aquí.
from rest_framework import viewsets
from .models import Producto, Cart, CartItem
from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    """
    Viewset para el modelo Producto.
    Permite a los usuarios ver, editar, crear y borrar productos.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# --- Vistas de páginas generales ---

def home_ferreteria(request):
    """
    Vista para la página principal.
    """
    productos = Producto.objects.filter(activo=True) # Obtiene todos los productos activos
    context = {
        'productos': productos
    }
    return render(request, 'productos/home.html', context)

def about_us(request):
    """
    Vista para la página 'Sobre Nosotros'.
    """
    return render(request, 'productos/about_us.html')

def productos_list(request):
    """
    Vista para la lista de productos amigable para el usuario.
    """
    productos = Producto.objects.filter(activo=True)
    context = {
        'productos': productos
    }
    return render(request, 'productos/productos_list.html', context)

# --- Funciones auxiliares para el carrito ---

def get_or_create_cart(request):
    """
    Función auxiliar para obtener o crear el carrito basado en la autenticación o la sesión.
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return cart

# --- Vistas del carrito de compras ---

def add_to_cart(request, producto_id):
    """
    Vista para añadir un producto al carrito.
    """
    producto = get_object_or_404(Producto, id=producto_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        messages.error(request, 'La cantidad debe ser al menos 1.')
        return redirect('productos_list')

    if producto.stock < quantity:
        messages.error(request, f'No hay suficiente stock para {producto.nombre}. Stock disponible: {producto.stock}')
        return redirect('productos_list')

    cart = get_or_create_cart(request) # Usamos la función auxiliar aquí

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        producto=producto,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, f'{quantity} x {producto.nombre} añadido al carrito.')
    return redirect('productos_list')

def cart_detail(request):
    """
    Vista para mostrar el contenido del carrito de compras.
    """
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()

    total_general = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'cart': cart,
        'total_general': total_general,
    }
    return render(request, 'productos/cart_detail.html', context)

def remove_from_cart(request, item_id):
    """
    Vista para eliminar un ítem específico del carrito.
    """
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart = get_or_create_cart(request)
        if cart_item.cart != cart:
            messages.error(request, "No tienes permiso para eliminar este artículo.")
            return redirect('cart_detail')

        cart_item.delete()
        messages.success(request, "Producto eliminado del carrito.")
    return redirect('cart_detail')

def update_cart_item(request, item_id):
    """
    Vista para actualizar la cantidad de un ítem en el carrito.
    """
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity'))

        cart = get_or_create_cart(request)
        if cart_item.cart != cart:
            messages.error(request, "No tienes permiso para actualizar este artículo.")
            return redirect('cart_detail')

        if quantity <= 0:
            cart_item.delete()
            messages.success(request, f"Producto '{cart_item.producto.nombre}' eliminado del carrito.")
        elif cart_item.producto.stock < quantity:
            messages.error(request, f'No hay suficiente stock para {cart_item.producto.nombre}. Stock disponible: {cart_item.producto.stock}')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"Cantidad de '{cart_item.producto.nombre}' actualizada a {quantity}.")
    return redirect('cart_detail')

@login_required # Opcional: Requiere que el usuario esté logueado para acceder al checkout
def checkout(request):
    """
    Vista para la página de checkout (dirección de envío y método de pago).
    """
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    total_general = sum(item.total_price for item in cart_items)

    if not cart_items:
        messages.warning(request, "Tu carrito está vacío. Añade productos antes de proceder al pago.")
        return redirect('cart_detail') # Redirigir si el carrito está vacío

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_general': total_general,
    }
    return render(request, 'productos/checkout.html', context)