from rest_framework import serializers

from .models import Category, Material


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, read_only=True)
    subcategories = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'code', 'total_price', 'materials', 'subcategories']

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data

    def get_total_price(self, obj):
        total = sum(obj.materials.values_list('price', flat=True))
        for subcategory in obj.subcategories.all():
            total += self.get_total_price(subcategory)

        return total
