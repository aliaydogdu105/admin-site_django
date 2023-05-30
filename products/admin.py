from django.contrib import admin
from .models import Product, Review, Category
from django.utils import timezone

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    classes = ('collapse',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "create_date", "is_in_stock", "update_date", "added_days_ago", "how_many_reviews")
    list_editable = ("is_in_stock",)
    list_filter = ("is_in_stock", "create_date")
    ordering = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug" : ("name",)}
    list_per_page = 25
    date_hierarchy = "update_date"
    inlines = (ReviewInline,)
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
            "fields" : ("description","categories"),
            'description' : "You can use this section for optionals settings"
        })
    )

    filter_horizontal = ("categories",)
    actions = ("is_in_stock", )
    

    def is_in_stock(self, request, queryset):
        count = queryset.update(is_in_stock=True)
        self.message_user(request, f"{count} types of products have been added to the stock.")

    is_in_stock.short_description = "Add marked products to stock"

    def added_days_ago(self, product):
        difference = timezone.now() - product.create_date
        return difference.days
    
    def how_many_reviews(self, obj):
        count = obj.reviews.count()
        return count


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_date', 'is_released')
    list_per_page = 50
    raw_id_fields = ('product',) 
    # # list_filter = ("product",)
    # list_filter = (
    #      ('product', RelatedDropdownFilter),
    # )
    # resource_class = ReviewResource

admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category)

admin.site.site_title = "My Admin Title"
admin.site.site_header = "My Admin Portal"
admin.site.index_title = "Welcome to My Admin Portal"
