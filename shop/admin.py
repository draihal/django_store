from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', ]
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


def get_photo_preview(obj):
    if obj.pk:
        return mark_safe(
            f"""<a href="{obj.image.url}" target="_blank">
            <img src="{obj.image.url}" alt="{obj.name}" style="max-width: 200px; max-height: 200px;" />
            </a>"""
        )
    return "None"


get_photo_preview.short_description = "Image preview 200px"


class ProductAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        'name', 'slug', 'price',
        'stock', 'available',
        'created_at', 'updated_at',
    ]
    list_filter = ['available', 'created_at', 'updated_at', ]
    list_editable = ['price', 'stock', 'available', ]
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 30
    readonly_fields = ("updated_at", "created_at", get_photo_preview)
    fieldsets = (
        ('Product info:', {
            'fields': (
                "category", ("name", "slug"),
                "description", "price",
                "available", "stock",
                "image", get_photo_preview,)
        }),
        (None, {
            'fields': ("updated_at", "created_at"),
        }),
    )


admin.site.register(Product, ProductAdmin)
