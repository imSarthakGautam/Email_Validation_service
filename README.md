

#  Email Validation API — Developer Notes

A Django REST Framework–based email validation tool inspired by services like **NeverBounce** or **ZeroBounce**.

---

##  Project Overview

The goal of this project is to build a **scalable backend system** that can:

1. Accept **single or batch** email addresses.
2. Validate email **syntax and domain structure**.
3. Verify **MX and SMTP** reachability.
4. Analyze **SPF, DKIM, and DMARC** DNS records.
5. Return results as structured JSON responses via REST API.

---
##  Setup & Environment

### 1. Initialize a Git Repository

```bash
git init
```

### 2. Activate Virtual Environment

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Git Bash or Linux/Mac
source venv/Scripts/activate
```

---
## 🗂️ Folder Structure

```
email_validation/
│
├── config/                     # Main Django project
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py / wsgi.py
│
├── core/                       # Main app logic
│   ├── migrations/
│   ├── serializers.py          # Input validation & output shaping
│   ├── services/               # Business logic layer
│   │   ├── email_syntax_service.py
│   │   ├── dns_service.py
│   │   ├── smtp_service.py
│   │   ├── domain_auth_service.py
│   ├── views.py                # REST API endpoints
│   ├── models.py               # (Optional if persistent storage later)
│
├── venv/
├── requirements.txt
└── manage.py
```

---

##  Architecture Overview

Flow of a single email request:

```
Client → Serializer → View → ValidationService → Response
```

### ValidationService (Core Steps)

| Step | Service                | What It Does                                           | Why It Matters                   |
| ---- | ---------------------- | ------------------------------------------------------ | -------------------------------- |
| 1    | `Email Syntax/Format`  | Checks format using regex & RFC rules                  | Filters junk input early         |
| 2    | `DNS service`          | Extracts domain, fetches MX records                    | Confirms domain can receive mail |
| 3    | `SMTP Service`         | Opens TCP connection to mail server, simulates RCPT TO | Confirms mailbox exists          |
| 4    | `Domain Auth Service`  | Checks SPF, DKIM, DMARC records                        | Detects spoofed/fake domains     |

---

##  How DNS Queries Work

We use:

```python
dns.resolver.resolve(domain, record_type)
```

### `record_type` determines what data you get:

| Record Type | Purpose                                                | Example Query                         | Example Response                        |
| ----------- | ------------------------------------------------------ | ------------------------------------- | --------------------------------------- |
| **A**       | Maps domain → IPv4 address                             | `resolve("google.com", "A")`          | `142.250.64.110`                        |
| **AAAA**    | Maps domain → IPv6 address                             | `resolve("google.com", "AAAA")`       | `2607:f8b0:4005:...`                    |
| **MX**      | Mail exchanger for domain (where to send email)        | `resolve("gmail.com", "MX")`          | `10 alt1.gmail-smtp-in.l.google.com.`   |
| **TXT**     | General text records — often used for SPF, DKIM, DMARC | `resolve("google.com", "TXT")`        | `"v=spf1 include:_spf.google.com ~all"` |
| **NS**      | Nameservers hosting the domain                         | `resolve("gmail.com", "NS")`          | `ns1.google.com.`                       |
| **CNAME**   | Canonical name alias                                   | `resolve("mail.google.com", "CNAME")` | `ghs.googlehosted.com.`                 |

Example:

```python
answers = dns.resolver.resolve("gmail.com", "MX")
for rdata in answers:
    print(rdata.exchange, rdata.preference)
```

Output:

```
alt1.gmail-smtp-in.l.google.com. 10
alt2.gmail-smtp-in.l.google.com. 20
```

Each record can have:

* `.exchange` → mail host name
* `.preference` → priority (lower = preferred)
* `.strings` → byte strings for TXT data

---

##  What MX Records Are

**MX (Mail Exchanger) records** tell which servers accept email for a domain.

Example:

```
gmail.com. IN MX 10 alt1.gmail-smtp-in.l.google.com.
```

Meaning:

* Gmail uses `alt1.gmail-smtp-in.l.google.com` to receive emails.
* The number `10` is priority (used if multiple servers exist).

Without an MX record, the domain **can’t receive emails** — which is a strong indicator the address is invalid.

---

##  Example Output Structure

Each email returns a structured report like:

```json
{
  "email": "user@example.com",
  "is_valid_syntax": true,
  "mx_records": [
    "alt1.gmail-smtp-in.l.google.com",
    "alt2.gmail-smtp-in.l.google.com"
  ],
  "smtp_status": "valid",
  "domain_auth": {
    "spf": true,
    "dkim": false,
    "dmarc": true
  }
}
```

For batch inputs:

```json
[
  {...}, {...}, {...}
]
```

---

##  Important Notes for Future Reference


  * DNS lookups can be slow — consider caching or using async DNS (like `aiodns`).
  * SPF, DKIM, DMARC are TXT-based checks under specific subdomains:

    * SPF → domain root (`example.com`)
    * DKIM → `<selector>._domainkey.example.com`
    * DMARC → `_dmarc.example.com`

* **SMTP Validation Notes**

  * Not all servers allow verification — some block probes or use “catch-all”.
  * Timeouts and retries are crucial.
  * Use sockets directly or libraries like `smtplib` or `validate_email`.

* **Scalability**

  * Batch validation via Celery or RQ background jobs.


* **DRF Serializer Role**

  * Input: ensures list of valid email strings.
  * Output: defines consistent JSON structure.


---

##  Using `curl` to Test API Endpoints


```bash
curl -X POST http://localhost:8000/api/validate-email/ \
  -H "Content-Type: application/json" \
  -d '{"email":"sarthak@mail.com"}'
```

Batch emails

```bash
curl -X POST http://localhost:8000/api/validate-emails/ \
  -H "Content-Type: application/json" \
  -d '{"emails": ["a@gmail.com", "b@yahoo.com"]}'
```

---

