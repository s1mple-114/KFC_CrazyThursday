from rest_framework import serializers
from .models import Order
from orderitem.models import OrderItem
from orderitem.serializers import OrderItemSerializer
import uuid
from django.utils import timezone
from django.db import transaction

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.ListField(write_only=True)
    order_items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user', 'total_amount', 'status', 'payment_method', 
                  'created_at', 'completed_time', 'items', 'order_items', 'user_name']
        # 添加只读字段，这些字段不应该由客户端提供
        read_only_fields = ['order_number', 'user', 'created_at', 'completed_time', 'status']
    
    @transaction.atomic
    def create(self, validated_data):
        # 提取items数据
        items_data = validated_data.pop('items', [])
        
        # 自动生成订单号
        if 'order_number' not in validated_data:
            validated_data['order_number'] = self.generate_order_number()
        
        # 自动设置当前用户
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        
        # 设置默认支付方式
        if 'payment_method' not in validated_data:
            validated_data['payment_method'] = 'ALIPAY'  # 默认支付宝
        
        # 设置默认状态
        validated_data['status'] = 'PENDING'
        
        # 创建订单
        order = super().create(validated_data)
        
        # 创建订单项
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                product_id=item_data.get('product_id'),
                quantity=item_data.get('quantity'),
                price=item_data.get('price')
            )
        
        return order
    
    def generate_order_number(self):
        """生成唯一的订单号"""
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        unique_id = uuid.uuid4().hex[:6].upper()
        return f"ORD{timestamp}{unique_id}"