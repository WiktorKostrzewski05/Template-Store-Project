from django.contrib import admin
from .models import Sub



class SubAdmin(admin.ModelAdmin):
    list_display = ['user', 'startDate', 'active']
    list_editable = ['startDate','active']

admin.site.register(Sub, SubAdmin)
