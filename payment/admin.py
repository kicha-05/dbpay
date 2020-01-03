from django.contrib import admin
from django.db import models
from . models import UserProfile,ProductModel,Cart



admin.site.register(ProductModel)
admin.site.register(Cart)

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name','email',)
    search_fields = ('name',)
    readonly_fields = ('name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(UserProfile,UserProfileAdmin)