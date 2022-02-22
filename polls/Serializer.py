
from rest_framework import serializers
from polls.models import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = What
        fields = "__all__"