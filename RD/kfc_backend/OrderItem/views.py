from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import orderitem
from .serializers import orderitemSerializer

class orderitemViewSet(viewsets.ModelViewSet):
    serializer_class = orderitemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return orderitem.objects.filter(order__user=self.request.user)
# Create your views here.
