# Create your views here.

from rest_framework import serializers
from rest_framework import generics
from rest_framework_recursive.fields import RecursiveField


from .models import Category


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class CategoryListSerializer(CategorySerializer):
    children = RecursiveField(many=True, required=False)

    def create(self, validated_data):
        to_create_list = [validated_data]
        root = None
        while to_create_list:
            to_create = to_create_list.pop()
            parent = to_create.get('parent')
            cat = Category.objects.create(name=to_create['name'])
            if parent:
                cat.parents.add(parent)
                cat.save()
            if root is None:
                root = cat
            children = to_create.get('children', [])
            for c in children:
                c['parent'] = cat
            to_create_list.extend(children)
        return root



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
