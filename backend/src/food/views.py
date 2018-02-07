from rest_framework import mixins, viewsets, permissions

from .models import FoodCategory, FoodItem
from .serializers import FoodCategorySerializer, FoodItemSerializer
from django.contrib.sites.shortcuts import get_current_site

class FoodItemsViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.prefetch_related('discount',
                                                 'category__discount',
                                                 'tags__discount', )
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}


class FoodCategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = FoodCategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return FoodCategory.objects.filter(site=get_current_site(self.request))
