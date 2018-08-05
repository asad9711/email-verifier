from dns import resolver
import smtplib
import ConfigParser
import os

config = ConfigParser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'cfg_data.conf'))

rcpt_mail_domain = config.get('data','domain_of_mail')
rcpt_mail_id = config.get('data', 'mail_id_to_validate')
sender_mail_id = config.get('data', 'sender_mail_id')

# TO know more about MX record of DNS server, refer
# https://www.slashroot.in/mx-record-dns-explained-example-configurations

dns_records = resolver.query(rcpt_mail_domain, 'MX')
mx_record = dns_records[0].exchange
mx_record = str(mx_record)

smtp_server = smtplib.SMTP()

smtp_server.set_debuglevel(0)

smtp_server.connect(mx_record)

if 'google' in mx_record:
 # "ehlo() and starttls() to be used for the case of smtp server of gmail"
    smtp_server.ehlo()
    smtp_server.starttls()

smtp_server.mail(sender=sender_mail_id)
status_code, resp_msg = smtp_server.rcpt(recip=rcpt_mail_id)
smtp_server.quit()

if status_code == 250:
    print 'mail-id %s is valid' % rcpt_mail_id
else:
    print 'mail-id %s is NOT valid' % rcpt_mail_id