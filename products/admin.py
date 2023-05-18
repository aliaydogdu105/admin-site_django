from django.contrib import admin
from .models import Product
from django.utils import timezone

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "create_date", "is_in_stock", "update_date")
    list_editable = ("is_in_stock",)
    list_filter = ("is_in_stock", "create_date")
    ordering = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug" : ("name",)}
    list_per_page = 25
    date_hierarchy = "update_date"
    # fields = (("name","slug"), "description","is_in_stock")
    fieldsets = (
        (None, {
            "fields": (
                ('name',"slug"), "is_in_stock" # to display multiple fields on the same line, wrap those fields in their own tuple
            ),
            # 'classes': ('wide', 'extrapretty'), wide or collapse
        }),
        ('My section', {
            "classes" : ("collapse", ),
            "fields" : ("description",),
            'description' : "You can use this section for optionals settings"
        })
    )

    actions = ("is_in_stock", )
    
    
    def is_in_stock(self, request, queryset):
        count = queryset.update(is_in_stock=True)
        self.message_user(request, f"{count} types of products have been added to the stock.")

    is_in_stock.short_description = "Add marked products to stock"

    def added_days_ago(self, product):
        difference = timezone.now() - product.create_date
        return difference.days



admin.site.register(Product, ProductAdmin)

admin.site.site_title = "My Admin Title"
admin.site.site_header = "My Admin Portal"
admin.site.index_title = "Welcome to My Admin Portal"
