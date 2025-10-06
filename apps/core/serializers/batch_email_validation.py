
from rest_framework import serializers

# class Serializers 1. single  email list
class BatchEmailSerializer(serializers.Serializer):
    emails = serializers.ListField(
        child= serializers.EmailField(),
        allow_empty=False
    )
 
