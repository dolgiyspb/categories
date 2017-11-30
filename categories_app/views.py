# Create your views here.

from rest_framework import serializers
from rest_framework import generics

from .models import Category


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class CategoryDetailSerializer(CategorySerializer):
    children = CategorySerializer(many=True)
    parents = CategorySerializer(many=True)
    siblings = CategorySerializer(read_only=True, many=True)


class CategoryList(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
