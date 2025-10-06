import re

EMAIL_REGEX= re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def is_email_format_valid(email):
    # regex check 
    return EMAIL_REGEX.match(email) is not None

def extract_domain_from_email(email):
    # split @ and return domain part: mail.com
    return email.split('@')[1].lower()