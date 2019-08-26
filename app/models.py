from app import db


class Import(db.Model):
    __tablename__ = 'Import'

    import_id = db.Column(db.Integer, primary_key=True)
    citizens = db.relationship('Citizen', backref='import')

class Citizen(db.Model):
    __tablename__ = 'Citizen'

    citizen_id = db.Column(db.Integer, primary_key=True)
    import_id = db.Column(db.ForeignKey('Import.import_id'), primary_key=True)

    town = db.Column(db.String)
    street = db.Column(db.String)
    building = db.Column(db.String)
    apartment = db.Column(db.Integer)
    name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String)
    relatives = db.Column(db.String)