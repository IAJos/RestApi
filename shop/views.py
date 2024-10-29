from rest_framework.viewsets import ReadOnlyModelViewSet
from shop.models import Category, Product, Article
from shop.serializers import CategoryDetailSerializer, CategoryListSerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class MultipleSerializerMixin:
    # Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent

    detail_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class

        return super().get_serializer_class()


class CategoryViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous pouvons maintenant simplement appeler la méthode disable
        self.get_object().disable()
        return Response()

    def get_queryset(self):
        return Category.objects.filter(active=True)

    # def get_serializer_class(self):
    #     # Si l'action demandée est retrieve nous retournons le serializer de détail
    #     if self.action == 'retrieve':
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()


class ProductViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Nous récupérons tous les produits dans une variable nommée queryset
        queryset = Product.objects.filter(active=True)
        # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset
