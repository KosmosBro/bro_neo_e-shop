from django.contrib import admin

# Register your models here.
from main.models import Cart, CartContent

admin.site.register(Cart)
admin.site.register(CartContent)
