from rest_framework import viewsets, mixins, permissions

from .models import Order, Gift
from .serializers import CheckoutSerializer, GiftSerializer, OrderSerializer
from django.contrib.sites.shortcuts import get_current_site


class OrdersViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Order.objects.filter(site=get_current_site(self.request))


class GiftsViewSet(viewsets.ModelViewSet):
    serializer_class = GiftSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return Gift.objects.filter(site=get_current_site(self.request))


class CheckoutViewset(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = CheckoutSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return Order.objects.filter(site=get_current_site(self.request))
