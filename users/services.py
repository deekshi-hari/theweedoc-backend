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
