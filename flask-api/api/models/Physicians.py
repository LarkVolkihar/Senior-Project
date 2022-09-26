from .. import db
from .ProviderModels import Provider, Office
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin


class Physician(UserMixin, db.Model):
    """Model for physicians."""

    __tablename__ = "Physician"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(
        db.String(200), primary_key=False, unique=False, nullable=False
    )
    provider_id = db.Column(db.Integer, db.ForeignKey("Provider.id"), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey("Office.id"), nullable=False)
    patients = db.relationship("Patient", backref="patients", lazy=True)
    phone_number = db.Column(db.String(16), index=True)
    pnumber_patients = db.relationship(
        "PNumbertoUser", backref="pnumber_patients", lazy=True
    )

    messages_sent = db.relationship(
        "Message",
        foreign_keys="Message.physician_sender_id",
        backref="sent_physician",
        lazy="dynamic",
    )

    messages_received = db.relationship(
        "Message",
        foreign_keys="Message.physician_sender_id",
        backref="received_physician",
        lazy="dynamic",
    )

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def set_creation_date(self):
        self.created_on = datetime.today()

    def set_last_login(self):
        self.last_login = datetime.today()
        db.session.commit()

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"Physician {self.name}"

    def serialize(self):
        return {
            "Physician_id": self.id,
            "Physician_name": self.name,
        }
