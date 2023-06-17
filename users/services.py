# from twilio.rest import Client
# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework.response import Response

# def send_sms(phone_number, message):
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     message = client.messages.create(
#         body=message,
#         from_=settings.TWILIO_PHONE_NUMBER,
#         to=phone_number
#     )

#     return Response({'message': 'SMS sent successfully.'})

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def __send_mail__(subject, template, context, from_email, to_mail):

    subject = subject
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    from_email = from_email
    to = to_mail

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
