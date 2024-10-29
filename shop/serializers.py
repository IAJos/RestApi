from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from shop.models import Category, Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'date_created', 'date_updated']


class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'date_created', 'date_updated']


class CategoryDetailSerializer(ModelSerializer):

    # products = ProductSerializer(many=True, read_only=True)
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'date_created', 'date_updated', 'products']

    def get_products(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.products.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProductSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data