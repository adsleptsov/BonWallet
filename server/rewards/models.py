from server.config import db

class CardRewards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(255), nullable=False)
    #- pointRewards: Array<PointRewards>
    additional_benefits = db.Column(db.JSON)
    offer_terms_url = db.Column(db.String(255))
    benefit_terms_url = db.Column(db.String(255))

class PointRewards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    multiplier = db.Column(db.Float, nullable=False)
    #- qualifyingLocation: Array<Qualifying>

'''
### Qualifying Protocol

- name: String

### QualifyingService Object extends Qualifying

- serviceType: String (food delivery, online shopping, etc.)

### QualifyingLocation Object extends Qualifying

- locationType: String (lodging, dining, supermarket, etc.)
'''
