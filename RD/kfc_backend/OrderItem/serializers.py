from rest_framework import serializers
from .models import orderitem

class orderitemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = orderitem
        fields = '__all__'