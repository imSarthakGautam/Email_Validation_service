#from .email_validation import validate_single_email, validate_batch_emails
from .format_validation import is_email_format_valid, extract_domain_from_email
from .dns_smtp_service import get_mx_records, smtp_verify_email
from .domain_auth_service import  get_dkim_valid, get_dmarc_valid, get_spf_valid


def validate_single_email(email:str)-> dict:
    """
    Dummy placeholder for single email validation logic.
    For now, returns a simple formatted response.
    """
    result = {
       "email": email,
        "format_valid": False,

        "domain": None,
        # "domain_valid": False,
        "mx_records": None,
        "smtp_status": None,

        "spf_valid": False,
        "dkim_valid": False,
        "dmarc_valid": False,

        "status": "unknown"
    }

    # VALIDATION PIPELINE 
    # format validation
    if not is_email_format_valid(email):
        result["status"]= "invalid_email_format"
        return result
    result["format_valid"]=True

    # Domain Extraction
    domain = extract_domain_from_email(email)
    if not domain:
        result["status"]= "invalid_domain"
        return result
    result["domain"]= domain

    # DNS Lookup
    mx_records = get_mx_records(domain)
    if mx_records:
        result["mx_records"]= mx_records
        result["domain_valid"]= True
        result["mx_found"]= True
    else:
        result["status"]= "no_mx_records"

    # SMTP Verification
    smtp_check_result= smtp_verify_email(mx_records, email)
    if smtp_check_result == "valid":
        result["smtp_status"] = "valid"
    elif smtp_check_result == "catch_all":
        result["smtp_status"] = "catch_all"
    else:
        result["smtp_status"] = "un-verfied"

    # Verify Domain Authentication Records (spf, dkim, dmarc)
    result["spf_valid"] = get_spf_valid(domain)
    result["dkim_valid"] = get_dkim_valid(domain)
    result["dmarc_valid"] = get_dmarc_valid(domain)


    # combine and format results into JSON like below format
    if result["smtp_status"] == "valid" and result["domain_valid"]:
        result["status"] = "valid"
    else:
        result["status"] = "invalid"

    # return {
    #     "email": email,
    #     "format_valid": True,
    #     "domain": email.split("@")[-1],
    #     "validation_steps": {
    #         "syntax_check": "passed",
    #         "dns_check": "pending",
    #         "smtp_check": "pending",
    #         "spf_check": "pending",
    #         "dkim_check": "pending",
    #         "dmarc_check": "pending",
    #     },
    #     "overall_status": "format_valid_only"
    # }

    return result
   



def validate_batch_emails(email_list: list[str])-> list[dict]:

    #job 

    results= []

    for email in email_list:
        results.append(validate_single_email(email))
    return results