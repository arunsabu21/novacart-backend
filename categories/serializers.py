from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    class Meta:
        model = Category
        fields = "__all__"