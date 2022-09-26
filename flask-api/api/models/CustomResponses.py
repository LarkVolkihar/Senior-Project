from .. import db

class CustomResponse(db.Model):
    __tablename__ = 'CustomResponse'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False, unique=True)
    response = db.Column(db.String(), nullable=False)

    def serialize(self):
        return {
            'name': self.name,
            'response': self.response
        }