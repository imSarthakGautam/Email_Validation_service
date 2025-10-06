import dns.resolver
import smtplib
import socket

def get_mx_records(domain):
    # using dns resolver, perform DNS query/fetch for MX records ---> returns mail server hostnames
    # MX Record: A DNS setting that tells where to deliver email for a domain
    try:
        resolved= dns.resolver.resolve(domain, 'MX')
        mx_hosts = [r.exchange.to_text().rstrip('.') for r in resolved]
        """
        r is dns.resolver.Answer object
        r.exchange is domain name of mail server
        rstrip('.') removes trailing .
        """
        return mx_hosts
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return False


"""
resolved =dns.resolver.Answer object
for r in resolved:
    print(r)

10 alt1.gmail-smtp-in.l.google.com.
20 alt2.gmail-smtp-in.l.google.com.
40 alt3.gmail-smtp-in.l.google.com.
30 alt4.gmail-smtp-in.l.google.com.
5 gmail-smtp-in.l.google.com. 


mx_hosts=
[
    'alt1.gmail-smtp-in.l.google.com',
    'alt2.gmail-smtp-in.l.google.com',
    'alt3.gmail-smtp-in.l.google.com',
    'alt4.gmail-smtp-in.l.google.com',
    'gmail-smtp-in.l.google.com'
]

"""


def smtp_verify_email(mx_records, email):
    """
    Attempts SMTP verification (check if specific email address actually exists on mail server) using MX records.
    Returns:
       "valid" → mailbox exists, email deliverable
       "invalid" → mailbox not found/ email rejected/undeliverable
       "catch_all" → domain/server accepts all emails
       "unreachable" → MX server not responding
    """
    if not mx_records :
        return "unreachable"
    
    # try connecting to each mail servers until one works or all fail
    for host in mx_records:
        try :

            server= smtplib.SMTP(timeout=8)
            server.connect(host) # open connection to mail server

            server.helo("example.com") #handshaking 
            server.mail("validator@example.com") #address
            code, response = server.rcpt(email) # verification step and listen 
            # code : 250, 550, 451 ; response : servers full msg string

            server.quit()

        # Interpret SMTP response codes
            if 200 <= code < 300:
                return "valid"
            elif 400 <= code < 500:
                return "catch_all"
            else:
                return "invalid"
    
        except (socket.timeout, socket.gaierror, smtplib.SMTPConnectError):
            continue
        except smtplib.SMTPServerDisconnected:
            continue
        except Exception:
            continue
    return "unreachable"




def _has_a_record(domain):
    # in case domain has A record is missing (fallback for missing MX)
    return

def _is_domain_valid():
    return