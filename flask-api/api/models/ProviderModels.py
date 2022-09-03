from .. import db

class Provider(db.Model):
    """Model class for provider. (Organization)"""
    
    __tablename__ = 'Provider'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    offices = db.relationship('Office', backref='provider', lazy = True)

    def serialize(self):

        data = {
            'id': self.id,
            'name': self.name,
            'offices': 'temp'
        }

        return data

class Office(db.Model):
    """Model for offices. """
    
    __tablename__ = 'Office'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    phone_number = db.Column(db.String(16), index=True)
    address = db.Column(db.String(128), index=True)
    city = db.Column(db.String(32), index=True)
    state = db.Column(db.String(16), index=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('Provider.id'), nullable=True)
    #physicians = db.relationship('Physician.id', backref='physicians', lazy=True)