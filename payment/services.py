from .models import UserProfile,UserValid,ProductModel,Cart,PrevOrder3
import razorpay
import datetime
from passlib.context import CryptContext




def encrypt(pw):
    pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000
    )
    return pwd_context.encrypt(pw)

def checkpass(pw, hashed):
    pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000
    )
    return(print(pwd_context.verify(pw, hashed)))




def haspo(uname):
        u = UserProfile.objects.get(name = uname)
        po = u.prevorder3_set.all()
        xl = []
        xl[:6] = [0] * 6
        for i in po:
            x=ProductModel.objects.get(item=i.item)        
            xl[x.catid]= xl[x.catid] + 1
            print(xl[x.catid])

        print("xxx")
        print(max(xl))
        print(xl.index(max(xl)))

        max_bought_cat_id = xl.index(max(xl))
        time = datetime.datetime.now()

        if time.hour == u.hot_hour:
            hot_hour = 1
        else:
            hot_hour = 0

        return(max_bought_cat_id,hot_hour)




def pay(total, cartowner, cartowneremail):
        
        print("inside payment")

        total = total+"00"

        #RAZORRRRRRRRRRRRRRRRRRRRRRRRRRR

        client = razorpay.Client(auth=("rzp_test_vCHW27HiXwl6yh", "lKJsTCxr1eRjEiJ81goOGUtd"))
        client.set_app_details({"title" : "Django", "version" : "3.0"})
        
        DATA = {
            "customer": {
                "name": cartowner,
                "email": cartowneremail,
                # "contact": "+919999888877"
            },
            "type": "link",
            "amount": total,
            "currency": "INR",
            "description": cartowner + "'s cart",
            "callback_url": "http://127.0.0.1:8000/paid",
            "callback_method": "get"
            }
        respone = client.invoice.create(data=DATA)

        invoice_id = respone['id']

        payurl = (respone['short_url'])
        print(payurl)
        return(payurl,invoice_id)

