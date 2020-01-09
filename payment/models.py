from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    name = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=255, unique=True)
    hot_hour = models.IntegerField(null=True)
    
    
    def __str__(self):
        return self.name

class UserValid(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class ProductModel(models.Model):
    item = models.CharField(max_length=30)
    price = models.IntegerField()
    category = models.CharField(max_length=30)
    catid = models.IntegerField()
    image = models.ImageField(null=True,blank=True,upload_to="pro-imgs/")

    def __str__(self):
        return self.item

class Cart(models.Model):

    # user = models.OneToOneField(
    # UserProfile,
    # on_delete=models.CASCADE,
    # primary_key=True)

    userprofile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,db_column = "cart_it")
    item = models.CharField(max_length=30)
    price = models.IntegerField()

    def __str__(self):
        return self.item


class PrevOrder3(models.Model):


    userprofile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,db_column = "prevorder_it")
    item = models.CharField(max_length=30)
    price = models.IntegerField()


    def __str__(self):
        return self.item


class secretid(models.Model):
    userprofile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,db_column = "s_no")
    sno = models.CharField(max_length=10)

    def __str__(self):
        return self.sno



# class PrevOrder2(models.Model):


#     userprofile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,db_column = "prevorder_it")
#     item = models.CharField(max_length=30)
#     price = models.IntegerField()


#     def __str__(self):
#         return self.item


