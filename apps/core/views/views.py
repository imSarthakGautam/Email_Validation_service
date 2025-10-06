from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# k k kura haru rest framework bata immport garna parxa

# import serializer, service function
from ..serializers import SingleEmailSerializer, BatchEmailSerializer
from ..services import validate_single_email, validate_batch_emails


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
        result = validate_single_email(email)
        return Response(result, status=status.HTTP_200_OK)


class BatchEmailValidationView(APIView):
    """
    POST /api/validate-emails/
    Body: {"emails": ["a@gmail.com", "b@yahoo.com"]}
    Returns: list of formatted results.
    """
    def post(self, request):
        serializer = BatchEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        emails = serializer.validated_data['emails']
        results = validate_batch_emails(emails)

        return Response(results, status=status.HTTP_200_OK)



