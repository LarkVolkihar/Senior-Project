from ..WebHelpers import WebHelpers
from flask_login import current_user, login_user
import logging
from ...models.Employees import Employee
from ...models.Admins import Admin
from ...models.Physicians import Physician
from ...models.Employees import Employee
from flask_session import Session
from flask import session
from functools import wraps



class Login:
    def login_employee(request):

        if current_user.is_authenticated:
            return WebHelpers.EasyResponse(
                current_user.name + " already logged in.", 400
            )

        email = request.form["email"]
        password = request.form["password"]
        # next_page = request.form['next_page']

        # Validate login attempt
        employee = Employee.query.filter_by(email=email).first()

        if employee and employee.check_password(password=password):
            # Employee exists and password matches password in db
            login_user(employee)
            employee.set_last_login()
            session["login_type"] = "employee"
            logging.debug(f"{employee.name} logged in.")

            return WebHelpers.EasyResponse(employee.name + " logged in.", 405)

        # Patient exists but password does not match password in db
        return WebHelpers.EasyResponse(
            "Invalid Employee email/password combination.", 405
        )

    def login_physician(request):

        if current_user.is_authenticated:
            return WebHelpers.EasyResponse(
                f"{current_user.name} already logged in.", 400
            )

        email = request.form["email"]
        password = request.form["password"]
        # next_page = request.form['next_page']

        # Validate login attempt
        physician = Physician.query.filter_by(email=email).first()

        if physician and physician.check_password(password=password):
            #  Patient exists and password matches password in db

            login_user(physician)
            physician.set_last_login()
            session["login_type"] = "physician"
            logging.debug(f"{physician.name} logged in.")

            return WebHelpers.EasyResponse(physician.name + " logged in.", 405)

        # Patient exists but password does not match password in db
        return WebHelpers.EasyResponse(
            "Invalid Physician email/password combination.", 405
        )

    def login_admin(request):

        if current_user.is_authenticated:
            return WebHelpers.EasyResponse(
                f"{current_user.name} already logged in.", 400
            )

        email = request.form["email"]
        password = request.form["password"]
        # next_page = request.form['next_page']

        # Validate login attempt
        admin = Admin.query.filter_by(email=email).first()

        if admin and admin.check_password(password=password):
            # Admin exists and password matches password in db

            login_user(admin)
            admin.set_last_login()
            session["login_type"] = "admin"
            logging.debug(f"{admin.name} logged in.")

            return WebHelpers.EasyResponse(admin.name + " logged in.", 405)

        # Admin exists but password does not match password in db
        return WebHelpers.EasyResponse("Invalid Admin email/password combination.", 405)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        login_type = session.get("login_type")
        if login_type == "admin":
            return f(*args, **kwargs)
        else:
            return f'"You need to be an admin to use this route."'

    return wrap


def physician_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        login_type = session.get("login_type")
        if login_type == "physician" or login_type == "admin":
            return f(*args, **kwargs)
        else:
            return f'"You need to be a physician or admin to use this route."'

    return wrap


def employee_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        login_type = session.get("login_type")
        if (
            login_type == "admin"
            or login_type == "physician"
            or login_type == "employee"
        ):
            return f(*args, **kwargs)
        else:
            return (
                f'"You need to be an employee, physician, or admin to use this route."'
            )

    return wrap
