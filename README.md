python -m venv venv
source venv/Scripts/activate


celery --> redis --> 


Features:
1. Single Email Verification

email input --> format validation ---> [ Verification Service ] 
REST API design

2. Bulk Email Verification
Scalability async queue


```python
dns.resolver.resolve(domain, record_type)
```
Here the parameter record_type tells what type of DNS records you want to retrieve for a given domain.
Common record types

| Record Type | Purpose                                                | Example Query                         | Example Response                        |
| ----------- | ------------------------------------------------------ | ------------------------------------- | --------------------------------------- |
| **A**       | Maps domain → IPv4 address                             | `resolve("google.com", "A")`          | `142.250.64.110`                        |
| **AAAA**    | Maps domain → IPv6 address                             | `resolve("google.com", "AAAA")`       | `2607:f8b0:4005:...`                    |
| **MX**      | Mail exchanger for domain (where to send email)        | `resolve("gmail.com", "MX")`          | `10 alt1.gmail-smtp-in.l.google.com.`   |
| **TXT**     | General text records — often used for SPF, DKIM, DMARC | `resolve("google.com", "TXT")`        | `"v=spf1 include:_spf.google.com ~all"` |
| **NS**      | Nameservers hosting the domain                         | `resolve("gmail.com", "NS")`          | `ns1.google.com.`                       |
| **CNAME**   | Canonical name alias                                   | `resolve("mail.google.com", "CNAME")` | `ghs.googlehosted.com.`                 |

