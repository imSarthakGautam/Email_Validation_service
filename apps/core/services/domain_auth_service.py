"""
DEEP VALIDATION LAYER
 Is this domain setup like real email sending domain or is it shady ?
"""

import dns.resolver

# sender policy framework
def get_spf_record(domain):
    """
    Purpose : Prevents spammers from sending emails using your domain (spoofing).
    Why needed : Shows whether the domain enforces sender authentication (good reputation indicator).
    How : Check if domain has a valid SPF record.
    """
    try:
        resolved= dns.resolver.resolve(domain, 'TXT')
        for rdata in resolved:
            if any("v=spf1" in txt for txt in rdata.strings):
                return True
    except Exception:
        pass
    return False

# domain Keys Identified Mail
def get_dkim_record(domain):
    """
    Purpose: Adds a cryptographic signature to emails to ensure message integrity and authenticity.
    Why needed: Verifies the sender and message werent tampered with — another trust signal.
    How : Check DKIM records, stored as <selector>._domainkey.<domain>.
    """
    common_selectors = ["default", "mail", "selector1", "s1"]
    for selector in common_selectors:
        try:
            dns.resolver.resolve(f"{selector}_domainkey.{domain}", "TXT")
            return True
        except dns.resolver.NoAnswer:
            continue
        except dns.resolver.NXDOMAIN:
            continue
        except Exception:
            continue
    return False

# Domain Based Message Authentication, Reporting and Conformance
def get_dmarc_record(domain):
    """
    Purpose: Defines a policy that tells receiving mail servers what to do when SPF/DKIM fail.
    Why needed: Protects the domains reputation and prevents phishing attacks using its name
    How : Check if domain has a DMARC record
    """
    try:
        resolved = dns.resolver.resolve(f"_dmarc.{domain}", 'TXT') 
        for rdata in resolved:
          if any("v=DMARC1" in txt for txt in rdata.strings):
           return True
    except Exception:
       pass
    return False
