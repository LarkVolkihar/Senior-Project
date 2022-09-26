from .TwilioClient import TwilioClient
from .SignUpHelpers import TwilioSignUpHelpers
from .MessageTracking import MessageTracking
from ..WebHelpers import WebHelpers
from twilio.base.exceptions import TwilioRestException
import logging
from flask import request
from ...models.ProviderModels import Provider, Office

class MessageHandling():


    def __init__(self, request):
        # get phone number and msg from twixml
        self.phone_number = request.values.get("From", None)
        self.body = request.values.get("Body", None)
        self.to = request.values.get("To", None)

        self.office = Office.query.filter_by(phone_number=self.to).first()
        self.provider_id = self.office.provider_id
        self.provider = Provider.query.get(self.provider_id)
        self.twilioClient = TwilioClient(self.provider.twilio_account_id, self.provider.twilio_auth_token)
    
    def SignupFlow(self):
        
        # logic for handling signup of new users
        try:
            # see if user has signed up and been accepted
            if TwilioSignUpHelpers.CheckIfAccepted(self.phone_number) == True:
                status_msg = f"Your physician has received your message."
                MessageTracking.create_new_message_patient(
                    phone_number=self.phone_number, body=self.body
                )
                self.twilioClient.send_message(
                    self.office.phone_number,
                    self.phone_number,
                    status_msg,
                )
                return WebHelpers.EasyResponse("Success.", 200)
            # if new, prepare db table for new account registration
            elif TwilioSignUpHelpers.CheckForNewUser(self.phone_number) == True:
                status_msg = TwilioSignUpHelpers.InitiateUserSignUp(self.phone_number, self.body)
                self.twilioClient.send_message(self.office.phone_number, self.phone_number, status_msg)
                return WebHelpers.EasyResponse("Success.", 200)
            # see if user has signed up but not accepted,
            elif TwilioSignUpHelpers.CheckIfRegistered(self.phone_number) == True:
                status_msg = (
                    f"Your physician is in the process of accepting your registration."
                )
                self.twilioClient.send_message(self.office.phone_number, self.phone_number, status_msg)
                return WebHelpers.EasyResponse("Success.", 200)
                # user has signed up but account not made yet, initiate signup form
            else:
                status_msg = TwilioSignUpHelpers.CreateNewUser(
                    phone_number=self.phone_number, msg=self.body
                )
                self.twilioClient.send_message(self.office.phone_number, self.phone_number, status_msg)
                return WebHelpers.EasyResponse("Success.", 200)
        except TwilioRestException as e:
            logging.warning(e)
            return WebHelpers.EasyResponse("Error", 400)