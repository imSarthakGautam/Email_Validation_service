# core/tasks/email_tasks.py
from celery import shared_task
from django.utils import timezone
from ..models import BatchJob, EmailValidationResult, BatchEmailResult
from ..services.email_validation import validate_single_email
from ..services.db_operations import save_email_validation_result, link_batch_result

"""
@param: job_id of batch job, emails
@return status on complete
"""
@shared_task(bind=True, max_retries=3, retry_backoff=True) #decorator sets this func as Celery Task
def process_batch_job(self, job_id, emails):
    try:
        # fetch BatchJob from DB by id
        job = BatchJob.objects.get(job_id=job_id)
        job.status = "IN_PROGRESS"
        job.started_at = timezone.now()
        job.save(update_fields=["status", "started_at"])

        completed = 0

        # iterating through each emails
        for email in emails:
            # validate each email
            result_dict = validate_single_email(email)
           
           # save or update validation result
            email_result = save_email_validation_result(email, result_dict)

            # link batch job and individual validation result of email
            link_batch_result(job, email_result)

            completed += 1
            job.completed_emails = completed
            job.save(update_fields=["completed_emails"])

        job.status = "COMPLETED"
        job.completed_at = timezone.now()
        job.save(update_fields=["status", "completed_at"])

        return {"job_id": job_id, "status": "COMPLETED", "processed": completed}

    except Exception as e:
        job = BatchJob.objects.filter(job_id=job_id).first()
        if job:
            job.status = "FAILED"
            job.save(update_fields=["status"])
        raise self.retry(exc=e)
