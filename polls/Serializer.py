
from rest_framework import serializers
from polls.models import *

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = "__all__"

    
    def to_representation(self, instance):
        print("wow")
        response = super().to_representation(instance)
        print(instance.name)
        city=Cities.objects.filter(country_id=instance.id)
        response["cities"]=[{"id":ct.id,"name":ct.name} for ct in city]

        return response
class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesProduct
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["product"]=instance.product.name
        return response