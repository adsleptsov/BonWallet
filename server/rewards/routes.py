from server.rewards import rewards_bp
from flask import Blueprint, jsonify, abort
from server.config import db
from server.rewards.models import CardRewards, PointRewards, QualifyingService, QualifyingLocation

# Getter for CardRewards by id
@rewards_bp.route('/card_rewards/<int:id>', methods=['GET'])
def get_card_rewards(id):
    card = CardRewards.query.get(id)
    if not card:
        return abort(404, description="CardRewards not found")
    
    return jsonify({
        'id': card.id,
        'card_name': card.card_name,
        'point_rewards': [pr.id for pr in card.point_rewards],  # Assuming you just want the IDs
        'additional_benefits': card.additional_benefits,
        'offer_terms_url': card.offer_terms_url,
        'benefit_terms_url': card.benefit_terms_url
    })

# Getter for PointRewards by id
@rewards_bp.route('/point_rewards/<int:id>', methods=['GET'])
def get_point_rewards(id):
    point = PointRewards.query.get(id)
    if not point:
        return abort(404, description="PointRewards not found")
    
    return jsonify({
        'id': point.id,
        'multiplier': point.multiplier,
        'qualifying': [q.id for q in point.qualifying]  # Assuming you just want the IDs
    })

# Getter for QualifyingService by id
@rewards_bp.route('/qualifying_service/<int:id>', methods=['GET'])
def get_qualifying_service(id):
    service = QualifyingService.query.get(id)
    if not service:
        return abort(404, description="QualifyingService not found")
    
    return jsonify({
        'id': service.id,
        'name': service.name,
        'service_type': service.service_type
    })

# Getter for QualifyingLocation by id
@rewards_bp.route('/qualifying_location/<int:id>', methods=['GET'])
def get_qualifying_location(id):
    location = QualifyingLocation.query.get(id)
    if not location:
        return abort(404, description="QualifyingLocation not found")
    
    return jsonify({
        'id': location.id,
        'name': location.name,
        'location_type': location.location_type
    })
