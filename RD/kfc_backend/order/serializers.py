from rest_framework import serializers
from .models import Order
from orderitem.serializers import OrderItemSerializer
import uuid
from django.utils import timezone

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        # 添加只读字段，这些字段不应该由客户端提供
        read_only_fields = ['order_number', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # 自动生成订单号
        if 'order_number' not in validated_data:
            validated_data['order_number'] = self.generate_order_number()
        
        # 自动设置当前用户
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)
    
    def generate_order_number(self):
        """生成唯一的订单号"""
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        unique_id = uuid.uuid4().hex[:6].upper()
        return f"ORD{timestamp}{unique_id}"