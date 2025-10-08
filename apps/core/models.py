# app/core/models.py

from django.db import models


class EmailValidationResult(models.Model):
    """
    represents result of validating single email
    stores validation status and data
    """
    email = models.EmailField(max_length=255)
    format_valid = models.BooleanField(default=False)
    
    # Technical results
    domain = models.CharField(max_length=255, blank=True, null=True)
    mx_records = models.JSONField(blank=True, null=True)     # store list of MX records
    smtp_status = models.CharField(max_length=100, blank=True, null=True)

    spf_valid = models.BooleanField(default=False)
    dkim_valid = models.BooleanField(default=False)
    dmarc_valid = models.BooleanField(default=False)
    
    status = models.CharField(max_length=255, blank=True, null=True)  # e.g. 'Invalid format', 'No MX record', etc.

    # Metadata
    checked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {'Valid' if self.is_valid else 'Invalid'}"


class BatchJob(models.Model):
    """
    represents validation requests of a batch
    to track request's lifecycle and status mgmt
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    job_id = models.CharField(max_length=100, unique=True)  # UUID for tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_emails = models.IntegerField(default=0)
    completed_emails = models.IntegerField(default=0)

    started_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Batch {self.job_id} - {self.status}"


class BatchEmailResult(models.Model):
    """
    Links Batch Job to individual email validation's result
    i.e. This email result belongs to this batch.
    1 Batch Job has many BatchEmail Result
    """
    batch_job = models.ForeignKey(BatchJob, on_delete=models.CASCADE, related_name='email_results')
    email_result = models.ForeignKey(EmailValidationResult, on_delete=models.CASCADE, related_name='batches')

    def __str__(self):
        return f"{self.email_result.email} in {self.batch_job.job_id}"
