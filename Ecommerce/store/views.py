from django.shortcuts import render
from rest_framework.decorators import api_view
from store.models import Product, Category
from store.serializers import ProductSerializer, CategorySerializer
from rest_framework.response import Responses

@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(featured=True)
    serialzer = ProductSerializer(products, many = True)
    return Response(serialzer.data)

