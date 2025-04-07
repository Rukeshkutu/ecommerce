from rest_framework import serializers
from store.models import Product, Variation, VariationManager, ReviewRating, Category

class CategorySerializer(serializers.ModelSerializer):
    # url = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug']
        extra_kwargs = {
            'slug': {'required':False}
        }
    # def get_url(self, obj):
    #     return self.context['request'].build_absolute_uri(
    #         reverse('products_by_category', args=[obj.slug])
    #     )


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ['id', 'vaiation_category', 'variation_value', 'is_active']

class ReviewRatingSerializer(serializers.ModelSerializer):
    users = serializers.StringRelatedField()
    class meta:
        model = ReviewRating
        fields = ['id', 'user', 'rating', 'review', 'created_at']
        read_only_files = ['user', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)
    vaiations = VariationSerializer(many=True, read_only=True)
    reviews = ReviewRatingSerializer(many = True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    in_cart = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'slug', 'description', 'price', 'image', 'stock',
            'category', 'average_rating', 'review_count', 'variations',
            'reviews', 'in_cart'
        ]
        lookup_field = 'slug'
        extra_kwargs = {'url' : {'lookup_field': 'slug'}}

    def get_average_rating(self, obj):
        return obj.averageReview()
    
    def get_review_count(self, obj):
        return obj.countReview()

    def get_in_cart(self, obj):
        request = self.context.get('revange')
        if request and request.user.is_authenticated:
            return obj.cartitem_set.filter(user=request.user).exists()
        return False
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Price cannot be negative')
        return value

class ReviewSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRating
        fields = ['rating','review']
        extra_kwargs = {
            'rating':{'min_value': 1, 'max_value': 5}
        }