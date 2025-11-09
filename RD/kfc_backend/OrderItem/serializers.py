from rest_framework import serializers
from .models import OrderItem
from order.models import Order
from product.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = OrderItem
        fields = '__all__'


class BatchOrderItemSerializer(serializers.Serializer):
    """
    批量创建订单项序列化器
    """
    order_id = serializers.IntegerField(required=True, help_text="订单ID")
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.Field(),
            required_fields=['product_id', 'quantity', 'price']
        ),
        min_length=1,  # 至少需要一个订单项
        help_text="订单项列表"
    )
    
    def validate_order_id(self, value):
        """验证订单是否存在"""
        try:
            order = Order.objects.get(id=value)
            # 可以添加更多的验证，比如订单状态是否允许添加订单项
            # if order.status != 'pending':
            #     raise serializers.ValidationError("该订单状态不允许添加订单项")
            return value
        except Order.DoesNotExist:
            raise serializers.ValidationError("订单不存在")
    
    def validate_items(self, value):
        """验证订单项列表"""
        for item in value:
            # 验证必要字段
            if 'product_id' not in item or 'quantity' not in item or 'price' not in item:
                raise serializers.ValidationError("每个订单项必须包含product_id, quantity和price字段")
            
            # 验证数量
            if int(item['quantity']) < 1:
                raise serializers.ValidationError("数量不能少于1")
            
            # 验证价格
            if float(item['price']) < 0:
                raise serializers.ValidationError("价格不能为负数")
            
            # 验证产品是否存在
            try:
                Product.objects.get(id=item['product_id'])
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"产品ID {item['product_id']} 不存在")
        
        return value
    
    def create(self, validated_data):
        """批量创建订单项"""
        order_id = validated_data['order_id']
        items_data = validated_data['items']
        order_items = []
        
        for item_data in items_data:
            # 创建订单项
            order_item = OrderItem.objects.create(
                order_id=order_id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                price=item_data['price']
            )
            order_items.append(order_item)
        
        # 更新订单总金额
        self._update_order_total(order_id)
        
        return order_items
    
    def _update_order_total(self, order_id):
        """更新订单总金额"""
        try:
            order = Order.objects.get(id=order_id)
            # 计算订单总金额
            total_amount = sum(item.price * item.quantity for item in OrderItem.objects.filter(order_id=order_id))
            order.total_amount = total_amount
            order.save(update_fields=['total_amount'])
        except Exception as e:
            # 记录错误但不中断流程
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"更新订单总金额失败：{str(e)}")