from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)

admin.site.site_title = "My Admin Title"
admin.site.site_header = "My Admin Portal"
admin.site.index_title = "Welcome to My Admin Portal"
