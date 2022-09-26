from flask import Blueprint, request, send_from_directory
from .. import login_manager
from flask_login import logout_user, login_required, current_user
from sqlalchemy import create_engine, MetaData
from flask import current_app as app, jsonify, session
from ..models.Messages import Message, db, PNumbertoUser
from ..services.WebHelpers import WebHelpers
from ..services.twilio.SignUpHelpers import TwilioSignUpHelpers
from ..services.twilio.MessageTracking import MessageTracking
import logging
from flask_cors import cross_origin
from twilio.twiml.messaging_response import MessagingResponse
from ..models.Patients import Patient
from ..services.twilio.TwilioClient import TwilioClient
from twilio.base.exceptions import TwilioRestException
from ..services.twilio.MessageTracking import MessageTracking
from ..models.ProviderModels import Office, Provider
from ..services.twilio.MessageHandling import MessageHandling


message_bp = Blueprint("message", __name__)


@message_bp.route("/api/message", methods=["GET"])
@login_required
@cross_origin()
def get_messages():
    """
    GET: Returns all messages.
    """

    if request.method == "GET":

        messages = Message.query.all()

        resp = jsonify([x.serialize() for x in messages])
        resp.status_code = 200

        return resp


@message_bp.route("/api/message/<int:id>", methods=["GET"])
@login_required
@cross_origin()
def get_message(id):
    """
    GET: Returns message with specified id.
    """

    if request.method == "GET":
        message = Message.query.get(id)
        if message is None:
            return WebHelpers.EasyResponse("Message with that id does not exist.", 404)

        resp = jsonify(message.serialize())
        resp.status_code = 200

        return resp


@message_bp.route("/api/message/", methods=["POST"])
@cross_origin()
def create_message():
    """
    POST: Creates new message.

    """
    msgHandler = MessageHandling(request)
    result = msgHandler.SignupFlow()
    return result
    

@message_bp.route("/api/message/<int:id>", methods=["DELETE"])
def delete_message(id):

    message = Message.query.filter_by(id=id).first()

    if request.method == "DELETE":
        if message:

            db.session.delete(message)
            db.session.commit()
            # return redirect('/api/message')
            logging.info(f"{message.name} deleted.")
            return WebHelpers.EasyResponse(f"{message.name} deleted.", 200)

        return WebHelpers.EasyResponse(f"message with that id does not exist.", 404)


@message_bp.route("/api/message/<int:id>", methods=["POST"])
def physician_message(id):

    if session["login_type"] == "physician":
        user = Patient.query.get(id)
        message = request.form["msg"]
        office_id = current_user.office_id
        office = Office.query.get(office_id)
        provider_id = office.provider_id
        provider = Provider.query.get(provider_id)
        twilioClient = TwilioClient(
            provider.twilio_account_id, provider.twilio_auth_token
        )

        if user:
            twilioClient.send_message(office.phone_number, user.phone_number, message)
            MessageTracking.create_new_message_physician_to_patient(
                current_user.id, user.phone_number, message
            )
            logging.warning(
                f"{current_user.name} sent a message to patient with id ({user.id})"
            )
            return WebHelpers.EasyResponse(f"Message sent.", 200)

        return WebHelpers.EasyResponse(f"User with id {id} does not exist.", 404)
