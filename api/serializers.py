from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from rest_framework import serializers

from main.models import Supplier, Discount, Category, Product, User, Comments, Cart,\
    CartContent


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'discount']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    discount = DiscountSerializer(many=True)
    supplier = SupplierSerializer(many=True)

    class Meta:
        model = Product
        fields = ['title', 'description', 'creation_date', 'picture', 'price', 'category', 'discount', 'supplier']

    def create(self, validated_data):
        create_category = validated_data.pop('category')
        create_discount = validated_data.pop('discount')
        create_supplier = validated_data.pop('supplier')
        product = Product.objects.create(**validated_data)

        for category in create_category:
            Category.objects.create(product=product, **category)

        for discount in create_discount:
            Discount.objects.create(product=product, **discount)

        for supplier in create_supplier:
            Supplier.objects.create(product=product, **supplier)
        return product


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def get_cart_records(self, cart=None, response=None):
        cart = self.get_cart() if cart is None else cart
        if cart is not None:
            cart_records = CartContent.objects.filter(cart_id=cart.id)
        else:
            cart_records = []

        if response:
            response.set_cookie('cart_count', len(cart_records))
            return response

        return cart_records

    def get_cart(self):
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            product = Product(id=self.request.COOKIES.get('product_id'))
            qty = 1
            try:
                cart = Cart.objects.get(user_id=user_id)
            except ObjectDoesNotExist:
                cart = Cart(user_id=user_id,
                            total_cost=0)
                cart.save()
                cart_content, _ = CartContent.objects.get_or_create(cart=cart, product=product)
                cart_content.qty = qty
                cart_content.save()

        else:
            session_key = self.request.session.session_key
            self.request.session.modified = True
            if not session_key:
                self.request.session.save()
                session_key = self.request.session.session_key
            try:
                cart = Cart.objects.get(session_key=session_key)
            except ObjectDoesNotExist:
                cart = Cart(session_key=session_key,
                            total_cost=0)
                cart.save()
        return cart


class CartContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartContent
        fields = '__all__'

    def get(self, request):
        cart = self.get_cart()
        cart_records = self.get_cart_records(cart)
        cart_total = cart.get_total() if cart else 0

        context = {
            'cart_records': cart_records,
            'cart_total': cart_total,
        }
        return render(request, 'cart.html', context)

    def post(self, request):
        product = Product.objects.get(id=request.POST.get('product_id'))
        cart = self.get_cart()
        quantity = request.POST.get('qty')
        cart_content, _ = CartContent.objects.get_or_create(cart=cart, product=product)
        cart_content.save()
        response = self.get_cart_records(cart, redirect('/#product-{}'.format(product.id)))
        product_id = product.id
        cart_content.qty = quantity
        response.set_cookie('qty', quantity)
        response.set_cookie('product_id', product_id)
        return response


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
