from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives, EmailMessage
from django.template.loader import get_template

EMAIL_SUBJECT_CHOICES = {
    'user_receipt': 'TitanFile Monthly Subscription Receipt',
    'paypal_api_error': 'Failed to renew a subscription',
}

def send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, headers=None):
    connection = connection or get_connection(username=auth_user,
                                    password=auth_password,
                                    fail_silently=fail_silently)
    headers = headers or {'Reply-To': from_email}
    return EmailMessage(subject, message, from_email, recipient_list,
                        connection=connection,
                        headers = headers).send()
                        
def send_mail_with_template(subject, from_email, recipient_list,
                            plaintext_template, html_template, context,
                            fail_silently=False, auth_user=None, auth_password=None,
                            connection=None, headers=None, bcc_list=None):
    connection = connection or get_connection(username=auth_user,
                                    password=auth_password,
                                    fail_silently=fail_silently)
    headers = headers or {'Reply-To': from_email}
    
    plaintext = get_template(plaintext_template)
    text_content = plaintext.render(context)
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list, bcc_list)
    if html_template is not None:
        html = get_template(html_template)
        html_content = html.render(context)
        msg.attach_alternative(html_content, "text/html")
    return msg.send()
