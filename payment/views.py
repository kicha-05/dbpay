from django.shortcuts import render
from rest_framework.views import APIView
from .models import UserProfile,UserValid,ProductModel,Cart,PrevOrder3
from rest_framework import status
from django.http import HttpResponse
from rest_framework.response import Response
from . serializers import UserSerializer,UserValidSerializer,ProductSerializer,CartSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib import messages
from django.db import IntegrityError
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import requests
from .services import haspo,pay
from urllib.parse import urlencode
import webbrowser
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import razorpay
import datetime



class Register(APIView):
    def get(self,request,format=None):
        return render(request, 'payment/register.html')




class UsersList(APIView):
    """List all the users"""
    def get(self,request,format=None):
        users = UserProfile.objects.all()
        serializer = UserSerializer(users, many=True)
        # UserProfile.objects.all().delete()
        return Response(serializer.data)
        
    def post(self,request,format=None):
        serializer = UserSerializer(data = request.data)
        #print(request.data.get("name"))
        if serializer.is_valid() :
            try:
                serializer.save()
                x = User.objects.create_user(username = request.data.get("name"), 
                password = request.data.get("password"), 
                email=request.data.get("email"))
                Token.objects.get_or_create(user=x)
                return render(request, 'payment/login.html')
            except:
                    pass            
        return Response("USER PROFILE WITH THE GIVEN CREDENTIALS ALREADY EXISTS")


class UserDetails(APIView):
    
    def get(self,request,pk,format=None):
        user = UserProfile.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self,request,pk,format=None):
        user = UserProfile.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
            user = UserProfile.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class UserValidView(APIView):

    def get(self,request,format=None):
        users = UserValid.objects.all()
        serializer = UserValidSerializer(users, many=True)
        return render(request, 'payment/login.html')
        
    def post(self,request,format=None):
      
        allusers = UserProfile.objects.all()
        temp = UserProfile.objects.get(name = request.data.get("name"))
        temp.save()
        comp = temp.password
        idie = str(temp.id)
        if comp == request.data.get("password"):
                if temp.name == "admin":
                    print("superuser detected")
                    admincontext = {
                        "users" : allusers
                    }
                    return render(request, 'payment/admin.html',
                    context=admincontext)

                else:
                    p = UserProfile.objects.get(pk=idie)
                    user = User.objects.get(username=p.name)
                    token = Token.objects.get(user=user)
                    # tok = "Token "+ token.key
                    
                    # prevorder check
                    poc = temp.prevorder3_set.all()
                    if poc is not None:
                        #max_bought_cat_id_rec = self.haspo(temp.name)
                        print(temp.name)
                        max_bought_cat_id_rec = haspo(temp.name)

                    print("recieved from the function")
                    ishothour = max_bought_cat_id_rec[1]
                    max_bought_cat_id_rec= max_bought_cat_id_rec[0]

                    #PRODUCT VIEW GET METHOD DUPLICATE STARTS
                    p = UserProfile.objects.get(pk=idie)
                    print(type(p.name))
                    #user = User.objects.all()
                    user = User.objects.get(username=p.name)
                    print("done")
                    produtcs = ProductModel.objects.all()
                    token = Token.objects.get(user=user)
                    print(token.key)
                    context = {
                        "products":produtcs,
                        "iden" : idie,
                        "tok" : token.key,
                        "max": max_bought_cat_id_rec,
                        "ishothour" : ishothour
                         
                    }
                    return render(request, 'payment/success.html',
                    context=context)                    

                    #PRODUCT VIEW GET METHOD DUPLICATE ENDS

        return render(request, 'payment/failure.html')
    

class ProductView(APIView):
    def get(self,request,pk,format=None):
        print("the user is")
        print(request.user)

        p = UserProfile.objects.get(pk=pk)
        print(type(p.name))
        #user = User.objects.all()
        user = User.objects.get(username=p.name)
        print("done")
        produtcs = ProductModel.objects.all()
        token = Token.objects.get(user=user)
        print(token.key)
        serializer = ProductSerializer(produtcs, many=True)
        con = {
            "products":produtcs,
            "iden" : pk,
            "tok" : token.key,
        }
        return render(request, 'payment/success.html',context=con)
    
    def post(self,request,format=None):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CartView(APIView):

    def get(self,request,pk,format=None):

        global inv_id_gb

        total = 0
        try: 
            c = Cart.objects.filter(userprofile=pk)
            serializer = CartSerializer(c, many=True)
            cartownerob = UserProfile.objects.get(pk=pk)
            cartowner = cartownerob.name
            cartowneremail = cartownerob.email

            for i in c:
                total = total +  i.price
        

        except Exception as e:
            print(e)

        ttl = str(total)
        if total != 0:
            payurl = pay(ttl, cartowner, cartowneremail)
            inv_id_gb = payurl[1]
            payurl = payurl[0]
        else:
            payurl = None

        context = {
            "cartitems" : c,
            "total" : total,
            "iden" : pk,
            "payurl" : payurl,
            "invoice_id" : inv_id_gb,
            
        }
        
        return render(request, 'payment/cart.html',context=context)
        
    def post(self,request,pk,format=None):

        u = UserProfile.objects.get(pk=pk)
        print(u)
        try:
            c = Cart.objects.create(item=request.data.get("item"),
            price=request.data.get("price"),userprofile=u)
            
            
            serializer = CartSerializer(data = request.data)
            if serializer.is_valid():
                return Response(serializer.data)
        except IntegrityError:
            return Response("ALREADY ITEM IN CART")

    def delete(self,request,pk,format=None):
        item = Cart.objects.filter(userprofile=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class sendmail(APIView):
    def get(self,request,format=None):
        try:
            send_mail(
                "hello from krishna",
                "hello this is dsadsadasdan test for the meail working method",
                'krishna@gmail.com',
                ['lomaroy243@mailart.ws'],
                fail_silently=False)
            return render(request , 'payment/sent.html')
        except:
            return Response("nope not sent")


class successredirect(APIView):

    def get(self,request,format=None):
        global inv_id_gb

        client = razorpay.Client(auth=("rzp_test_vCHW27HiXwl6yh",
                                     "lKJsTCxr1eRjEiJ81goOGUtd"))
        client.set_app_details({"title" : "Django", "version" : "3.0"})
        invoice = client.invoice.fetch(inv_id_gb)

        # print(invoice)

        paid_at= invoice['paid_at']

        print("neeededddddd")

        print(paid_at)

        paid_at_time = datetime.datetime.fromtimestamp(paid_at)
        print(paid_at_time)

        hour = paid_at_time.hour

        name = invoice['customer_details']['name']

        print(name)

        if invoice['status'] == "paid":
            cartpaid = True
        else:
            cartpaid = False

        if cartpaid:
            try:
                u = UserProfile.objects.get(name=name)

                ci = u.cart_set.all()

                print(u.hot_hour)
                u.hot_hour = hour
                u.save()

                print(ci)

                for i in ci:
                    try:
                        u.prevorder3_set.create(item=i.item,price=i.price)
                    except:
                        Response("PREVIOUS ORDER LIST NOT CREATED FOR -" + i.item)
            except:
                print("NO PREVIOUS ORDER CREATED")
        return render(request, 'payment/paysuccess.html')

class Orders(APIView):
    def get(self,request,pk,format=None):

        x = UserProfile.objects.get(id=pk)
        response = x.prevorder3_set.all()

        con = {
            "response" : response,
        }

        return render(request, 'payment/cartbs.html' , context=con)










    #  1577959322