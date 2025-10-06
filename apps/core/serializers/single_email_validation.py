# import serializers
from rest_framework import serializers

# class Serializers inheriting from parent class Serializer of serializers module of DRF
class SingleEmailSerializer(serializers.Serializer):
    email= serializers.EmailField()