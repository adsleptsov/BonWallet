from server.config import db

card_points = db.Table('card_points',
    db.Column('card_id', db.Integer, db.ForeignKey('CardRewards.id'), primary_key=True),
    db.Column('point_id', db.Integer, db.ForeignKey('PointRewards.id'), primary_key=True)
)

point_qualifying = db.Table('point_qualifying', 
    db.Column('point_id', db.Integer, db.ForeignKey('PointRewards.id'), primary_key=True),
    db.Column('qualifying_id', db.Integer, db.ForeignKey('Qualifying.id'), primary_key=True)
)

class CardRewards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(255), nullable=False)
    point_rewards = db.relationship('PointRewards', 
                                    secondary=card_points, 
                                    lazy='subquery', 
                                    backref=db.backref('cards', lazy=True))
    additional_benefits = db.Column(db.JSON)
    offer_terms_url = db.Column(db.String(255))
    benefit_terms_url = db.Column(db.String(255))

class PointRewards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    multiplier = db.Column(db.Float, nullable=False)
    qualifying = db.relationship('Qualifying',
                                 secondary=point_qualifying,
                                 lazy='subquery',
                                 backref=db.backref('points', lazy=True))

class Qualifying(db.Model):
    __abstract__ = True  # Abstract class, won't be created in the database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

# QualifyingService class, extending Qualifying
class QualifyingService(Qualifying):
    __tablename__ = 'qualifying_service'
    service_type = db.Column(db.String(255), nullable=False)

# QualifyingLocation class, extending Qualifying
class QualifyingLocation(Qualifying):
    __tablename__ = 'qualifying_location'
    location_type = db.Column(db.String(255), nullable=False)
