from django.contrib import admin
from django.template.loader import render_to_string

# Register your models here.

from products import models


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'img',
        'name',
        'category',
        'product_marker',
        'now_price',
        'old_price',
        'created',
        'modified'
    ]

    list_filter = [
        'category',
        'product_marker',
        'created',
        'modified'
    ]

    search_fields = [
        'name',
        'short_text',
        'long_text',
    ]

    fieldsets = (
        (
            None, {'fields': ('name', 'category')}
        ),
        (
            'Marker&Image', {'fields': ('product_marker', 'image', )}
        ),
        (
            'Price', {'fields': ('old_price', 'now_price')}
        ),
        (
            'Content', {'fields': ('short_text', 'long_text')}
        )
    )

    def img(self, obj):
        return render_to_string(
            'products/components/img.html',
            {'image': obj.image.img.url}
        )


admin.site.register(models.Category)
admin.site.register(models.ProductMarker)
admin.site.register(models.Product, ProductAdmin)
