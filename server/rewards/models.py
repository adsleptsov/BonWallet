from server.config import db

card_points = db.Table('card_points',
    db.Column('card_id', db.Integer, db.ForeignKey('card_rewards.id'), primary_key=True),
    db.Column('point_id', db.Integer, db.ForeignKey('point_rewards.id'), primary_key=True)
)

point_qualifying = db.Table('point_qualifying', 
    db.Column('point_id', db.Integer, db.ForeignKey('point_rewards.id'), primary_key=True),
    db.Column('qualifying_id', db.Integer, db.ForeignKey('qualifying.id'), primary_key=True)
)

class CardRewards(db.Model):
    __tablename__ = 'card_rewards'
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
    __tablename__ = 'point_rewards'
    id = db.Column(db.Integer, primary_key=True)
    multiplier = db.Column(db.Float, nullable=False)
    qualifying = db.relationship('Qualifying',
                                 secondary=point_qualifying,
                                 lazy='subquery',
                                 backref=db.backref('points', lazy=True))

class Qualifying(db.Model):
    __tablename__ = 'qualifying'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(50))  # Discriminator column

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'qualifying',
        'with_polymorphic': '*'
    }

class QualifyingService(Qualifying):
    __tablename__ = 'qualifying_service'
    id = db.Column(db.Integer, db.ForeignKey('qualifying.id'), primary_key=True)
    service_type = db.Column(db.String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'service'
    }

class QualifyingLocation(Qualifying):
    __tablename__ = 'qualifying_location'
    id = db.Column(db.Integer, db.ForeignKey('qualifying.id'), primary_key=True)
    location_type = db.Column(db.String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'location'
    }
