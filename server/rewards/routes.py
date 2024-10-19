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


@rewards_bp.route('/qualifying/<int:id>', methods=['GET'])
def get_qualifying(id):
    qualifying = Qualifying.query.get(id)
    if not qualifying:
        return abort(404, description="Qualifying not found")
    
    response = {
        'id': qualifying.id,
        'name': qualifying.name,
        'type': qualifying.type  # This will be either 'service' or 'location'
    }

    # If it's a service, include service_type
    if qualifying.type == 'service':
        response['service_type'] = qualifying.service_type
    
    # If it's a location, include location_type
    elif qualifying.type == 'location':
        response['location_type'] = qualifying.location_type
    
    return jsonify(response)
