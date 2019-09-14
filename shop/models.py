from django.db import models
from django.urls import reverse

from .mixins import TimestampMixin


class Category(TimestampMixin):
    name = models.CharField(
        max_length=150, db_index=True,
        help_text='Name for category',)
    slug = models.SlugField(
        max_length=150, db_index=True,
        unique=True, help_text='Slug for url',)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(TimestampMixin):
    category = models.ForeignKey(
        Category, related_name='products',
        on_delete=models.CASCADE,)
    name = models.CharField(
        max_length=100, db_index=True,
        help_text='Name for product',)
    slug = models.SlugField(
        max_length=100, db_index=True,
        help_text='Slug for url',)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def upload_product_image_dir(self, filename):
        url = f'products_images/{self.category}/{filename.lower()}'
        return url
    image = models.ImageField(upload_to=upload_product_image_dir, blank=True)

    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
