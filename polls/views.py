from django.shortcuts import render
from msrest import Serializer
from rest_framework.views import APIView
from polls.models import *
from rest_framework.response import Response
from polls.Serializer import *
# Create your views here.
from django.db.models import Sum,Max
from decouple import config
from django.http import HttpResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.conf import settings
import requests
import json
import jwt
import pandas as pd
from mysite.settings import SECRET_KEY
TOKEN_URL=config('TOKEN_URL')

# i just put my functions here so that you can see it all in one space but honestly i can create a new file for the functions
def generate(user, username, password):
    payload = {
        "agentId": user.id,
        "username": username,
        "password": password,
    }
    
    url = settings.TOKEN_URL
    url_response = requests.post(url, payload)
    response = json.loads(url_response.text)
    return response

def blackListToken(request):
    token = request.headers['Authorization'].split(' ')[1]
    t, created = BlackListedToken.objects.get_or_create(token=token)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def decode_token(request):
    token = request.headers['Authorization'].split(' ')[1]
    decoded_token = jwt.decode(token, options={'verify_signature': False})
    return decoded_token

def isTokenValid(request):
    token = request.headers['Authorization'].split(' ')[1]
    t = BlackListedToken.objects.filter(token=token)
    if len(t) > 0:
        return False

    return True


def validate_decoded_token(request):
    decodedToken = decode_token(request)
    user_id = decodedToken['user_id']

    if not isTokenValid(request):
        return False, decodedToken

    try:
        user = User.objects.get(pk=user_id)
        if user:
            return True, decodedToken
    except:
        return False, decodedToken

# First part is for the authentication and logout of users
class LoginView(APIView):

    def post(self, request):
        email = request.data["email"]
    
        password = request.data["password"]
        query = User.objects.all()
   
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return Response({"status": "Failed", "message": "We don't recognize this user with that username.",
                            "error_message": str(e)})

        if user:    
            if not user.is_active:
                return Response({"status": "Failed", "message": "This user is not active."})
            if not user.check_password(password):
                return Response({"status": "Failed", "message": "Password is incorrect."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            token = Token.objects.get(user=user)
            if token:
                access_token = generate(user, user.username, password)
        else:
            return Response({"status": "Failed", "message": "This user doesn't exists."})
      
        return Response({
                        "token": access_token["access"],"user_id":user.id}, status=status.HTTP_202_ACCEPTED)
   
       
class LogoutView(APIView):

    def get(self, request):
        blackListToken(request)
        return Response(status=status.HTTP_200_OK)

#For the countries VIew
class CountryView(APIView):
    def get(self,request):
        print("here")
        country = Countries.objects.all()
        print(country)
        serializer=CountrySerializer(country,many=True,context={"request": request})
        print(serializer)
        return Response(serializer.data)

#this is for editing the user
    
class EditUserView(APIView):
    def patch(self,request,id=None):
        isTokenValid, decoded_token = validate_decoded_token(request)
        if not isTokenValid:
            return Response({"status": "failed", "message": "You are not authorized to view this page. Token is invalid."},
                            status=status.HTTP_401_UNAUTHORIZED)
        agentId = decoded_token["user_id"]
        current_agent = User.objects.get(pk=agentId)
        current_agent.email=request.data["email"]
        current_agent.first_name=request.data["first_name"]
        current_agent.last_name=request.data["last_name"]
        current_agent.save()
        up=UserProfile.objects.get(user=current_agent)
        up.age=request.data["age"]
        country=Countries.objects.get(pk=int(request.data["country"]))
        up.countries=country
        city=Cities.objects.get(pk=int(request.data["country"]))
        up.cities=city
        up.save()
        return Response(status=status.HTTP_200_OK)

# This part is for the User part the first View will be for the get whole and add new sales 
class SalesUserView(APIView):
    def get(self,request):
        isTokenValid, decoded_token = validate_decoded_token(request)
        if not isTokenValid:
            return Response({"status": "failed", "message": "You are not authorized to view this page. Token is invalid."},
                            status=status.HTTP_401_UNAUTHORIZED)
        agentId = decoded_token["user_id"]
        current_agent = User.objects.get(pk=agentId)
        sales=SalesProduct.objects.filter(user=current_agent)
        serializer=SalesSerializer(sales,many=True,context={"request": request})
        return Response(serializer.data)

    def post(self,request,id=None):
        isTokenValid, decoded_token = validate_decoded_token(request)
        if not isTokenValid:
            return Response({"status": "failed", "message": "You are not authorized to view this page. Token is invalid."},
                            status=status.HTTP_401_UNAUTHORIZED)
        agentId = decoded_token["user_id"]
        current_agent = User.objects.get(pk=agentId)
        prod=Product.objects.filter(name=request.data["product"])
        user=User.objects.get(pk=int(request.data["user_id"]))
        sales=SalesProduct.objects.create(
        
        
        product=prod[0],
        
        revenue=request.data["revenue"],
        
        sales_number=request.data["sales_number"],
        
        date=request.data["date"],
        
        user=user)
        sales.save()
        serializer=SalesSerializer(sales,context={"request": request})
        return Response(serializer.data,status=status.HTTP_201_CREATED)
class NewSalesUserView(APIView):
    def delete(self,request,id=None):
        isTokenValid, decoded_token = validate_decoded_token(request)
        if not isTokenValid:
            return Response({"status": "failed", "message": "You are not authorized to view this page. Token is invalid."},
                            status=status.HTTP_401_UNAUTHORIZED)

        sales=SalesProduct.objects.get(pk=id).delete()
   
        return Response(status=status.HTTP_204_NO_CONTENT)



    def patch(self,request,id=None):
        isTokenValid, decoded_token = validate_decoded_token(request)
        if not isTokenValid:
            return Response({"status": "failed", "message": "You are not authorized to view this page. Token is invalid."},
                            status=status.HTTP_401_UNAUTHORIZED)
        agentId = decoded_token["user_id"]
        current_agent = User.objects.get(pk=agentId)
        sales=SalesProduct.objects.get(pk=id)
        data=request.data.keys()
        print(data)
        if "product" in data:
            prod=Product.objects.filter(name=request.data["product"])
            sales.product=prod[0]
        if "revenue" in data:
            sales.revenue=request.data["revenue"]
        if "sales_number" in data:
            sales.sales_number=request.data["sales_number"]
        if "date" in data:
            sales.date=request.data["date"]
        if "user_id" in data:
            user=User.objects.get(pk=int(request.data["user_id"]))
            sales.user=user
        sales.save()
        serializer=SalesSerializer(sales,context={"request": request})
        return Response(serializer.data,status=status.HTTP_200_OK)


    def put(self,request,id=None):
        isTokenValid, decoded_token = validate_decoded_token(request)
        if not isTokenValid:
            return Response({"status": "failed", "message": "You are not authorized to view this page. Token is invalid."},
                            status=status.HTTP_401_UNAUTHORIZED)
        agentId = decoded_token["user_id"]
        current_agent = User.objects.get(pk=agentId)
        sales=SalesProduct.objects.get(pk=id)
        
        prod=Product.objects.filter(name=request.data["product"])
        sales.product=prod[0]
        
        sales.revenue=request.data["revenue"]
        
        sales.sales_number=request.data["sales_number"]
        
        sales.date=request.data["date"]
        user=User.objects.get(pk=int(request.data["user_id"]))
        sales.user=user
        sales.save()
        serializer=SalesSerializer(sales,context={"request": request})
        return Response(serializer.data,status=status.HTTP_200_OK)

class SalesView(APIView):
    def get(self,request):
        
        isTokenValid, decoded_token = validate_decoded_token(request)
        if not isTokenValid:
            return Response({"status": "failed", "message": "You are not authorized to view this page. Token is invalid."},
                            status=status.HTTP_401_UNAUTHORIZED)
        agentId = decoded_token["user_id"]
        current_agent = User.objects.get(pk=agentId)
        sum=SalesProduct.objects.filter(user=current_agent).aggregate(Sum('sales_number'))
        revenue=SalesProduct.objects.filter(user=current_agent).aggregate(Sum('revenue'))
        sumall=SalesProduct.objects.aggregate(Sum('sales_number'))
        revenueall=SalesProduct.objects.aggregate(Sum('revenue'))
        highrevenue= SalesProduct.objects.filter(user=current_agent)
        
        highre = SalesProduct.objects.latest('revenue')
        print(highre)
        products=Product.objects.all()
        
        max=0
        max1=0
        for g in products:
            print(g)
            tempsum=SalesProduct.objects.filter(user=current_agent,product=g).aggregate(Sum('revenue'))
            if tempsum['revenue__sum']>max:
                max=tempsum['revenue__sum']
                tally={"product_name":g.name,"price":max}
            tempmax=SalesProduct.objects.filter(user=current_agent,product=g).aggregate(Sum('sales_number'))
            if tempmax['sales_number__sum']>max1:
                max=tempmax['sales_number__sum']
                tally1={"product_name":g.name,"price":max}
        print(tally1)    
        return Response({"average_sales_for_current_user":revenue["revenue__sum"]/sum["sales_number__sum"],"average_sales_all_user":revenueall["revenue__sum"]/sumall["sales_number__sum"], "highest_revenue_sale_for_current_user":{"sale_id":highre.id,"revenue":highre.revenue},"product_highest_revenue_for_current_user":{"product_name":tally["product_name"],"price":tally["price"]},"product_highest_sales_number_for_current_user":{"product_name":tally1["product_name"],"price":tally1["price"]}})


class UploadCountryAndCityView(APIView):
    def post(self,request):
        try:
            file = request.FILES['file']
            print(file)
            pandas=pd.read_csv(file)
            print(pandas)
            for index, row in pandas.iterrows():
                country,created=Countries.objects.get_or_create(name=row['Country'])
                city=Cities.objects.create(name=row['City'],country=country)
            return Response(status=status.HTTP_200_OK)
        except:
            print("waw")

class UploadSalesView(APIView):
    def post(self,request):
        try:
            file = request.FILES['file']
            print(file)
            pandas=pd.read_csv(file)
            print(pandas)
            for index, row in pandas.iterrows():
                prod,created=Product.objects.get_or_create(name=row['product'])
                sp=SalesProduct.objects.create(sales_number=row['sales_number'],revenue=row['revenue'],product=prod,date=row['date'] )
            return Response(status=status.HTTP_200_OK)
        except:
            print("waw")