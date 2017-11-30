# Create your views here.

from rest_framework import serializers
from rest_framework import generics
from rest_framework_recursive.fields import RecursiveField


from .models import Category


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class CategoryListSerializer(CategorySerializer):
    children = serializers.ListField(child=RecursiveField(), required=False)

    def create(self, validated_data):
        pass

    def _make_category(self, category, parent=None):
        pass


class CategoryDetailSerializer(CategorySerializer):
    children = CategorySerializer(many=True)
    parents = CategorySerializer(many=True)
    siblings = CategorySerializer(read_only=True, many=True)


class CategoryList(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
