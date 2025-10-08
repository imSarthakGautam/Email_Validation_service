# import serializers
from rest_framework import serializers
from ..models import EmailValidationResult

# class Serializers inheriting from parent class Serializer of serializers module of DRF
class SingleEmailSerializer(serializers.Serializer):
    email= serializers.EmailField()


class EmailValidationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model= EmailValidationResult
        fields = [
            'id',

            'email',
            'format_valid',
            
            'domain',
            'mx_records',
            'smtp_status',

            'spf_valid',
            'dkim_valid',
            'dmarc_valid',
            
            'status',

            'checked_at',
            'updated_at',
        ]
"""
{
  "id": 42,
  "email": "user@example.com",
  "format_valid": true,

  "domain": "example.com",
  "mx_records": ["mx1.example.com", "mx2.example.com"],
   "smtp_status": "valid",

  "spf_valid": "valid",
  "dkim_valid": "missing",
  "dmarc_valid": "invalid",

   "status": "SMTP verified",
  
  "checked_at": "2025-10-06T15:45:12Z"
}
"""