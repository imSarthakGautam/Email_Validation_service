
from rest_framework import serializers
from ..models import BatchEmailResult, BatchJob, EmailValidationResult
from .single_email_validation import EmailValidationResultSerializer


# class Serializers 1. single  email list
class BatchEmailSerializer(serializers.Serializer):
    emails = serializers.ListField(
        child= serializers.EmailField(),
        allow_empty=False
    )
 
class BatchEmailResultSerializer(serializers.ModelSerializer):
    # nested serializer ( this email result belongs to this batch)
  #  email_result = EmailValidationResultSerializer(read_only=True)

  #  email_result_id = serializers.PrimaryKeyRelatedField(           # for POST
  #       queryset=EmailValidationResult.objects.all(),
  #       source='email_result',  # map this to the actual FK field
  #       write_only=True
  #   )
   class Meta:
        model = BatchEmailResult
        fields = ['id', 'email_result', 'email_result_id']


class BatchJobSerializer(serializers.ModelSerializer):
    # batch job result--> JSON
    email_results= BatchEmailResultSerializer(many=True, read_only=True)

    class Meta:
        model = BatchJob
        fields = [
            'job_id',
            'status',
            'total_emails',
            'completed_emails',
            'created_at',
            'completed_at',
            'email_results',
        ]
        
    def get_results(self, obj):
        return EmailValidationResultSerializer(
            [r.email_result for r in obj.results.all()], many=True
        ).data
"""
{
  "job_id": "a1b2c3",
  "status": "COMPLETED",
  "total_emails": 3,
  "completed_emails": 3,
  "created_at": "2025-10-06T10:00:00Z",
  "completed_at": "2025-10-06T10:01:10Z",
  "email_results": [
    {
      "id": 1,
      "email_result": {
        "email": "a@gmail.com",
        "format_valid": true,
        "domain_valid": true,
        ...
      }
    },
    {
      "id": 2,
      "email_result": {
        "email": "b@yahoo.com",
        ...
      }
    }
  ]
}
"""


