from django.contrib import admin
from .models import Category, Template, Type, Style


class Lists(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Category, Lists)
admin.site.register(Type, Lists)
admin.site.register(Style, Lists)



class TemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'price',
                    'description', 'created', 'updated', 'pro']
    list_editable = ['price', 'pro']
    list_per_page = 20


admin.site.register(Template, TemplateAdmin)
