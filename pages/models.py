from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import uuid


class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse('templates_by_category', args=[self.id])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Type(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Style(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Template(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ManyToManyField(Type, blank=True)
    style = models.ManyToManyField(Style, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='template_images', blank=True)
    image_thumbnail = ImageSpecField(source='image', processors=[
                                     ResizeToFill(500, 500)], format='JPEG', options={'quality': 100})
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    pro = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'template'
        verbose_name_plural = 'templates'

    def get_absolute_url(self):
        return reverse('template_detail', args=[self.category.id, self.id])

    def __str__(self):
        return self.name
