from ..models import EmailValidationResult, BatchEmailResult
from ..serializers import EmailValidationResultSerializer, BatchEmailResultSerializer

def save_email_validation_result(email, result_dict):
    """
    Create or update an EmailValidationResult for a given email.
    """
    # Find the last saved record
    existing = EmailValidationResult.objects.filter(email=email).last()

    # Create or update
    if existing:
        for key, value in result_dict.items():
            setattr(existing, key, value)
        existing.save()
        return existing
    else:
        serializer = EmailValidationResultSerializer(data=result_dict)

    serializer.is_valid(raise_exception=True)
    return serializer.save()




def link_batch_result(batch_job, email_result):
    """
    Link validated email with its batch job record.
    """
    data = {"batch_job": batch_job, "email_result": email_result}
    serializer = BatchEmailResultSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
