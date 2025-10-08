# from django.shortcuts import render
# k k kura haru rest framework bata immport garna parxa
from rest_framework.views import APIView     # base class import
from rest_framework.response import Response # Python Data to JSON output
from rest_framework import status            # For Status Codes
from rest_framework.generics import RetrieveAPIView

import uuid

# import serializer, service function
from ..serializers import SingleEmailSerializer, BatchEmailSerializer, BatchJobSerializer, EmailValidationResultSerializer
from ..services.email_validation import validate_single_email, validate_batch_emails

from ..models import EmailValidationResult, BatchJob
from ..tasks.email_taks import process_batch_job

class SingleEmailValidationView(APIView):
    """
    POST /api/validate-email/
    Body : { "email" : "sarthak@mail.com"}
    Response : Formatted validation structure
    """
    def post(self, request):
        # deserialize input
        serializer = SingleEmailSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)

        email= serializer.validated_data['email']

        try:
            result = validate_single_email(email)     
        except Exception as e:
            print(f"Error during email validation for {email}: {e}") # Log the error
            return Response(
                {"detail": "Email validation service failed."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        result_serializer= EmailValidationResultSerializer(data=result)
        result_serializer.is_valid(raise_exception=True)
        # store results into DB for persistence : EmailValidationResult
        result_serializer.save()

        return Response(result_serializer.data, status=status.HTTP_200_OK)
       


class BatchEmailValidationView(APIView):
    """
    POST /api/validate-emails/
    Body: {"emails": ["a@gmail.com", "b@yahoo.com"]}
    Returns: list of formatted results.
    """
    def post(self, request):
        serializer = BatchEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        emails = serializer.validated_data['emails'] # python lists, emails = []

        # assign job for asynchrounous operation
        job_id= str(uuid.uuid4())
        job = BatchJob.objects.create(
            job_id=job_id,
            total_emails= len(emails),
            status="PENDING"
        )
        print('API endpoint hit')
        process_batch_job.delay(job_id, emails) # run asynchronously via .delay

        results = validate_batch_emails(emails) # dispatch Celery Task

        # store batch job results in DB : BatchJob

        return Response(results, status=status.HTTP_200_OK)



class BatchJobStatusView(RetrieveAPIView):
    """
    GET /api/jobs/<job_id>/
    """
    lookup_field = "job_id"
    queryset = BatchJob.objects.all()
    serializer_class = BatchJobSerializer