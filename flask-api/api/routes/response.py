from flask import Blueprint, request
from flask import current_app as app, jsonify
from ..models.CustomResponses import CustomResponse, db
from ..services.WebHelpers import WebHelpers
import logging
from flask_cors import cross_origin
from flask_login import current_user
from ..services.auth.login import admin_required, employee_required, physician_required

response_bp = Blueprint("response_bp", __name__)


@response_bp.get("/api/response")
@employee_required
@cross_origin()
def get_responses():
    """
    Returns all responses.
    """

    responses = CustomResponse.query.all()
    resp = jsonify([x.serialize() for x in responses])
    resp.status_code = 200
    logging.info(f"{current_user.name} accessed all responses.")
    return resp


@response_bp.get("/api/response/<int:id>")
@employee_required
@cross_origin()
def get_response(id):
    """
    GET: Returns Response with specified id.
    """

    response = CustomResponse.query.get(id)
    if response is None:
        return WebHelpers.EasyResponse("Response with that id does not exist.", 404)
    resp = jsonify(response.serialize())
    resp.status_code = 200
    logging.info(f"{current_user.name} accessed response with id of {id}.")

    return resp

@response_bp.post("/api/response")
@employee_required
def create_office():
    """
    POST: Creates new response.
    """
    name = request.form['name']
    response = request.form['response']

    custom_response = CustomResponse(
        name=name,
        response=response
    )

    db.session.add(custom_response)
    db.session.commit()
    logging.debug(f"New response {custom_response.name} created.")

    return WebHelpers.EasyResponse(f"New response {custom_response.name} created.", 201)


@response_bp.put("/api/response/<int:id>")
@physician_required
@cross_origin()
def update_response(id):
    """
    PUT: Updates specified response with new message.
    """
    response = CustomResponse.query.filter_by(id=id).first()
    old_name = response.name

    if response:
        response.response = request.form['response']
        db.session.commit()

        logging.warning(
            f"{current_user.name} updated response with id {response.id}."
        )
        return WebHelpers.EasyResponse(f"Response message updated.", 200)
    return WebHelpers.EasyResponse(f"Response with that id does not exist.", 404)


@response_bp.delete("/api/response/<int:id>")
@admin_required
@cross_origin()
def delete_response(id):
    """
    Deletes response with specified id.
    """

    response = CustomResponse.query.get(id)
    response_name = response.name
    response_id = response.id

    if response:
        db.session.delete(response)
        db.session.commit()
        logging.warning(
            f"{current_user.name} deleted response with id {response_id} and name of {response_name}."
        )
        return WebHelpers.EasyResponse(f"{response.name} deleted.", 200)
    return WebHelpers.EasyResponse(f"response with that id does not exist.", 404)
