# productos/serializers.py

from rest_framework import serializers
from .models import Producto # Importa tu modelo Producto

class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Producto.
    Convierte objetos Producto a JSON y viceversa.
    """
    class Meta:
        model = Producto # Especifica el modelo al que se asocia este serializador
        fields = '__all__' # Indica que quieres serializar todos los campos del modelo
        # Opcional: Si solo quisieras algunos campos, podrías hacer:
        # fields = ['id', 'nombre', 'precio', 'stock']