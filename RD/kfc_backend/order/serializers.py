from rest_framework import serializers
from .models import Order
from orderitem.serializers import orderitemSerializer

class OrderSerializer(serializers.ModelSerializer):
    items = orderitemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'