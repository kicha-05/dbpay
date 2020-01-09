from django.contrib import admin
from django.db import models
from . models import UserProfile,ProductModel,Cart,secretid
from django import forms


admin.site.register(ProductModel)
admin.site.register(Cart)

# Register your models here.

x = UserProfile.objects.all().first()

class secretidForm(forms.ModelForm):
    model = secretid
    fields = ['sno']

        
class UserProfileAdmin(admin.ModelAdmin):
    
    form =  secretidForm  
    
    def getatt(self,obj):
        print(obj)
        return null

    list_display = ('name','email','getatt')
    search_fields = ('name','email')
    readonly_fields = ('name',)


    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    
   

    
    # 
    # list_display = ('x',)

admin.site.register(UserProfile,UserProfileAdmin)