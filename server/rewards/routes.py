from server.rewards import rewards_bp
import os
from flask import Blueprint, jsonify, abort, request, render_template
from server.config import db, PARENT_DIR 
from server.rewards.models import CardRewards, PointRewards, QualifyingService, QualifyingLocation
from server.restaurant_scraper import get_merchants_data, extract_single_reward_data, API_URL  # Assuming your scraper file is named scraper.py
from werkzeug.security import check_password_hash
import re

def verify_password_from_file(password):
    try:
        with open(os.path.join(PARENT_DIR, 'pw_hashes.txt'), 'r') as f:
            hashes = f.readlines()

        # Check the password against each hash in the file
        for hash_line in hashes:
            hash_line = hash_line.strip()  # Remove any newline characters
            if check_password_hash(hash_line, password):
                return True

        return False  # Return False if no match is found

    except FileNotFoundError:
        abort(500, description="Password hashes file not found")

@rewards_bp.route('/add_card', methods=['GET', 'POST'])
def add_card_rewards():
    if request.method == 'GET':
        # Serve the HTML form when accessed via GET
        return render_template('add_card.html')

    elif request.method == 'POST':
        # Check if the request is JSON or form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        # Extract the password and other fields
        password = data.get('password')
        card_name = data.get('card_name')
        additional_benefits = data.get('additional_benefits')
        offer_terms_url = data.get('offer_terms_url')
        benefit_terms_url = data.get('benefit_terms_url')
        qualifying_ids = data.get('qualifying_ids')  # This will be a comma-separated string

        # Verify the password using the verify_password_from_file function
        if not verify_password_from_file(password):
            return abort(403, description="Invalid password")

        # Create the new CardRewards entry
        new_card_rewards = CardRewards(
            card_name=card_name,
            additional_benefits=additional_benefits,
            offer_terms_url=offer_terms_url,
            benefit_terms_url=benefit_terms_url
        )
        db.session.add(new_card_rewards)
        db.session.commit()

        # If qualifying IDs are provided, associate the qualifying objects with the new CardRewards
        if qualifying_ids:
            qualifying_ids = [int(id.strip()) for id in qualifying_ids.split(',') if id.strip()]
            for qualifying_id in qualifying_ids:
                qualifying = Qualifying.query.get(qualifying_id)
                if qualifying:
                    # Add the qualifying object to the card's point rewards relationship
                    for point_reward in qualifying.points:
                        new_card_rewards.point_rewards.append(point_reward)
                else:
                    return abort(400, description=f"Qualifying ID {qualifying_id} does not exist")
            db.session.commit()

        # Return success response
        return jsonify({
            'message': 'CardRewards added successfully',
            'card_name': new_card_rewards.card_name,
            'qualifying_ids': qualifying_ids
        })


@rewards_bp.route('/add_point_rewards', methods=['GET', 'POST'])
def add_point_rewards():
    if request.method == 'GET':
        # Serve the HTML form when accessed via GET
        return render_template('add_point_rewards.html')
    
    elif request.method == 'POST':
        # Check if the request is JSON or form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        # Extract the password and other fields
        password = data.get('password')
        multiplier = data.get('multiplier')
        qualifying_ids = data.get('qualifying_ids')  # This will be a comma-separated string
        card_id = data.get('card_id')  # Optional card_id input

        # Verify the password using the verify_password_from_file function
        if not verify_password_from_file(password):
            return abort(403, description="Invalid password")

        # Create the new PointRewards entry
        new_point_rewards = PointRewards(multiplier=multiplier)
        db.session.add(new_point_rewards)
        db.session.commit()

        # If qualifying IDs are provided, associate the qualifying objects with the new PointRewards
        if qualifying_ids:
            qualifying_ids = [int(id.strip()) for id in qualifying_ids.split(',') if id.strip()]
            for qualifying_id in qualifying_ids:
                qualifying = Qualifying.query.get(qualifying_id)
                if qualifying:
                    new_point_rewards.qualifying.append(qualifying)
                else:
                    return abort(400, description=f"Qualifying ID {qualifying_id} does not exist")
            db.session.commit()

        # If a card ID is provided, associate the new PointRewards with the specified CardRewards
        if card_id:
            card = CardRewards.query.get(card_id)
            if card:
                card.point_rewards.append(new_point_rewards)  # Associate the point rewards with the card
                db.session.commit()
            else:
                return abort(400, description=f"Card ID {card_id} does not exist")

        # Return success response
        return jsonify({
            'message': 'PointRewards added successfully',
            'multiplier': new_point_rewards.multiplier,
            'qualifying_ids': qualifying_ids,
            'card_id': card_id
        })



@rewards_bp.route('/add_qualifying', methods=['GET', 'POST'])
def add_qualifying():
    if request.method == 'GET':
        # Serve the HTML form when accessed via GET
        return render_template('add_qualifying.html')
    
    elif request.method == 'POST':
        # Check if the request is JSON or form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        # Extract the password and other fields
        password = data.get('password')
        name = data.get('name')
        qualifying_type = data.get('type')
        point_id = data.get('point_id')  # Extract the point_id from the request

        # Verify the password using the verify_password_from_file function
        if not verify_password_from_file(password):
            return abort(403, description="Invalid password")

        # Validate the point_id and ensure it exists
        point = PointRewards.query.get(point_id)
        if not point:
            return abort(400, description="Invalid point_id provided")

        # Based on qualifying_type, create the appropriate subclass
        if qualifying_type == 'service':
            service_type = data.get('service_type')
            if not service_type:
                return abort(400, description="Service type is required for qualifying services")
            new_qualifying = QualifyingService(name=name, service_type=service_type)

        elif qualifying_type == 'location':
            location_type = data.get('location_type')
            if not location_type:
                return abort(400, description="Location type is required for qualifying locations")
            new_qualifying = QualifyingLocation(name=name, location_type=location_type)

        else:
            return abort(400, description="Invalid qualifying type")

        # Add the new Qualifying (Service or Location) to the database
        db.session.add(new_qualifying)
        db.session.commit()

        # Link the Qualifying object with the specified PointRewards object
        point.qualifying.append(new_qualifying)
        db.session.commit()

        # Return success response
        return jsonify({
            'message': 'Qualifying added successfully',
            'name': new_qualifying.name,
            'type': qualifying_type,
            'point_id': point_id,
            'service_type': getattr(new_qualifying, 'service_type', None),
            'location_type': getattr(new_qualifying, 'location_type', None)
        })


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


# Endpoint to check if a user is at a qualifying location
@rewards_bp.route('/check_rewards', methods=['POST'])
def check_rewards():
    try:
        # Extract longitude and latitude data from the incoming JSON request
        user_data = request.get_json()
        latitude = user_data.get('latitude')
        longitude = user_data.get('longitude')

        if not latitude or not longitude:
            return jsonify({"error": "Longitude and/or latitude data is missing"}), 400

        # Combine latitude and longitude into the expected format: "latitude,longitude"
        user_location = f"{latitude},{longitude}"

        # Validate the combined location format
        if not is_valid_location(user_location):
            return jsonify({"error": "Invalid location format"}), 400

        # Use the existing functions to get and extract reward data
        data = get_merchants_data(API_URL, user_location)
        merchants = data.get("merchants", [])
        reward_data = extract_single_reward_data(merchants)

        if reward_data:
            return jsonify(reward_data), 200
        else:
            return jsonify({}), 200  # Empty JSON response if no location matches the criteria

    except Exception as e:
        return jsonify({"error": "An internal server error occurred"}), 500

    import re

def is_valid_location(location):
    # Regular expression for latitude, longitude validation
    pattern = r'^-?\d{1,2}(\.\d+)?,\s?-?\d{1,3}(\.\d+)?$'
    return bool(re.match(pattern, location))

