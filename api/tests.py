from rest_framework.test import APITestCase

from io import BytesIO
from PIL import Image
from django.core.files.base import File

from main.models import User, Category, Discount, Supplier, Product


class TestCategoryApi(APITestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_superuser(email='kos@mail.ru', password='1234')

    def test_user_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/register/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_user_add_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/register/'

        data = {
            'email': 'tur@mai.ru',
            'first_name': 'Tur',
            'last_name': 'Kosmos',
            'password': "1234",

        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_user_update_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/register/'

        data = {
            'email': 'tur@mai.ru',
            'first_name': 'Turanss',
            'last_name': 'Kosmosss',
            'password': "1234",

        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_user_delete_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/register/'

        data = {
            'email': 'tur@mai.ru',
            'first_name': 'Turanss',
            'last_name': 'Kosmosss',
            'password': "1234",

        }

        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, 204)

    def test_user_api_fail(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/register/'

        data = {
            'email': 12,
            'first_name': 'Turanss',
            'last_name': 'Kosmosss',
            'password': "1234",

        }

        with self.assertRaises(TypeError):
            User.objects.create(data, url)


class TestProductApi(APITestCase):

    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_superuser(email='kos@mail.ru', password='1234')
        cls.category = Category.objects.create(title='Category')
        cls.discount = Discount.objects.create(discount=12)
        cls.supplier = Supplier.objects.create(name='Supplier')

    def test_product_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/product/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_product_add_api(self):

        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/product/'

        data = {
            'title': 'Banana',
            'description': 'Fruit',
            'creation_date': '18.07.2022, 11:01',
            'price': 111,
            'picture': 'picture.png',
            'category': [self.category.id],
            'discount': [self.discount.id],
            'supplier': [self.supplier.id],

        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_product_update_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/product/'

        data = {
            'title': 'Banana',
            'description': 'Fruit',
            'creation_date': '18.07.2022, 11:01',
            'price': 111,
            'picture': 'picture.png',
            'category': [self.category.id],
            'discount': [self.discount.id],
            'supplier': [self.supplier.id],
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_product_delete_api(self):
        self.client.login(email='kos@mail.ru', password='1234')
        self.product = Product.objects.create(title='dssds', id=2, price=12)

        url = '/api/product/2/'

        data = {
            'title': 'Banana',
            'description': 'Fruit',
            'creation_date': '18.07.2022, 11:01',
            'price': 111,
            'picture': 'picture.png',
            'category': [self.category.id],
            'discount': [self.discount.id],
            'supplier': [self.supplier.id],

        }

        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, 204)

    def test_product_api_fail(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/register/'

        data = {
            'title': 'Banana#$#@',
            'description': 'Fruit',
            'creation_date': '18.07.2022, 11:01',
            'price': "111",
            'picture': 'picture.png',
            'category': [self.category.id],
            'discount': [self.discount.id],
            'supplier': [self.supplier.id],

        }

        with self.assertRaises(TypeError):
            Product.objects.create(data, url)


class TestSupplierApi(APITestCase):

    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_superuser(email='kos@mail.ru', password='1234')
        cls.product = Product.objects.create(title='dssds', id=2, price=12)

    def test_supplier_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/supplier/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_supplier_add_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/supplier/'

        data = {
            'name': 'Kos',
            'product': [self.product.id],

        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_supplier_update_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/supplier/'

        data = {
            'name': 'Kos',
            'product': [self.product.id],
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_product_delete_api(self):
        self.client.login(email='kos@mail.ru', password='1234')
        self.product = Supplier.objects.create(name='kos', product=self.product, id=1)

        url = '/api/supplier/1/'

        data = {
            'name': 'Kos',
            'product': [self.product.id],

        }

        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, 204)

    def test_supplier_api_fail(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/supplier/'

        data = {
            'name': 121212,
            'product': [self.product.id],

        }

        with self.assertRaises(TypeError):
            Supplier.objects.create(data, url)


class TestDiscountApi(APITestCase):

    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_superuser(email='kos@mail.ru', password='1234')
        cls.product = Product.objects.create(title='dssds', id=2, price=12)

    def test_discount_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/discount/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_discount_add_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/discount/'

        data = {
            'discount': 12,
            'product': [self.product.id],

        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_discount_update_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/discount/'

        data = {
            'discount': 1,
            'product': [self.product.id],
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_discount_delete_api(self):
        self.client.login(email='kos@mail.ru', password='1234')
        self.discount = Discount.objects.create(discount=12, product=self.product, id=1)

        url = '/api/discount/1/'

        data = {
            'discount': 1,
            'product': [self.product.id],

        }

        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, 204)

    def test_discount_api_fail(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/discount/'

        data = {
            'name': '121212',
            'product': [self.product.id],

        }

        with self.assertRaises(TypeError):
            Discount.objects.create(data, url)


class TestCategoryApi(APITestCase):

    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_superuser(email='kos@mail.ru', password='1234')
        cls.product = Product.objects.create(title='dssds', id=2, price=12)

    def test_category_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/category/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_category_add_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/category/'

        data = {
            'title': 'KOsmos',
            'description': 'KOsmos',
            'product': [self.product.id],

        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_category_update_api(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/category/'

        data = {
            'title': 'KOsmos',
            'description': 'KOsmos',
            'product': [self.product.id],
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_category_delete_api(self):
        self.client.login(email='kos@mail.ru', password='1234')
        self.category = Category.objects.create(title='KOsmos', description='sddsds', product=self.product, id=1)

        url = '/api/category/1/'

        data = {
            'title': 'KOsmos',
            'description': 'KOsmos',
            'product': [self.product.id],

        }

        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, 204)

    def test_category_api_fail(self):
        self.client.login(email='kos@mail.ru', password='1234')

        url = '/api/category/'

        data = {
            'title': 1221,
            'description': 'KOsmos',
            'product': [self.product.id],

        }

        with self.assertRaises(TypeError):
            Discount.objects.create(data, url)
