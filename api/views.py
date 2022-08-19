from django.http import JsonResponse
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import CategorySerializer, \
    DiscountSerializer, SupplierSerializer, ProductSerializer, UserSerializer, CommentsSerializer, CartSerializer, \
    CartContentSerializer
from main.models import Category, Discount, Supplier, Product, User, Comments, Cart, \
    CartContent


class CreateUserAPIView(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get(self, request):
        cart = Cart.objects.all()
        title = request.query_params.get('title', None)
        if title is not None:
            cart = cart.filter(title__icontains=title)

        movie_serializer = CartSerializer(cart, many=True)
        return JsonResponse(movie_serializer.data, safe=False)

    def post(self, request):
        cart = request.data
        serializer = CartSerializer(data=cart)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        data = request.data
        count = Cart.objects.filter(user=data["user"]).delete()
        return JsonResponse({'message': '{} Cart were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


class CartContentViewSet(viewsets.ModelViewSet):
    queryset = CartContent.objects.all()
    serializer_class = CartContentSerializer

    def get(self, request):
        cart_content = CartContent.objects.all()
        title = request.query_params.get('title', None)
        if title is not None:
            cart_content = cart_content.filter(title__icontains=title)

        movie_serializer = CartSerializer(cart_content, many=True)
        return JsonResponse(movie_serializer.data, safe=False)

    def post(self, request):
        cart_content = request.data
        serializer = CartContentSerializer(data=cart_content)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        data = request.data
        count = CartContent.objects.filter(cart=data["cart"], product=data["product"], qty=data["qty"],
                                           id=data["id"]).delete()
        return JsonResponse({'message': '{} CartContent were deleted successfully!'.format(count[0])},

                            status=status.HTTP_204_NO_CONTENT)


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
