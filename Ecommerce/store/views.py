from django.shortcuts import render
from django.db.models import Q
from store.models import Product, ReviewRating
from store.serializers import ProductSerializer, ReviewSubmitSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.
@api_view(['GET', 'POST'])
#@permission_classes([IsAdminUser])
def product_list(self):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data, context={'request':request})
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    queryset = Product.objects.filter(is_available=True)
    #filter
    category_slug = request.query_params.get('category')
    if category_slug:
        queryset = queryset.filter(category_slug = category_slug)
    #search
    search_query = request.query_params.get('search')
    if search_query:
        queryset= queryset.filter(
            Q(product_name__icontains = search_query) | 
            Q(description__icontains = search_query)
        )
    
    serializer = ProductSerializer(queryset, many=True, context = {'request':request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(
            category__slug=category_slug,
            slug=product_slug,
            is_available=True
        )
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, partial=True, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data)