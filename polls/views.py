from django.shortcuts import render
from rest_framework.views import APIView
from polls.models import *
from rest_framework.response import Response
from polls.Serializer import *
# Create your views here.
from django.http import HttpResponse
from rest_framework import status


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class PostViewSet(APIView):
    def get(self,request):
        queryset=What.objects.all()
        print(queryset)
        serializer1=PostSerializer(queryset,many=True)
        print(serializer1.data)
        return Response({"status": "success",
                                "message": "Call Center Settings list retrieved.",
                                "data": serializer1.data},
                            status=status.HTTP_200_OK)