import requests
import json

# Define constants for API endpoint
API_URL = "https://eataroundtown.marriott.com/api/v2/Merchants/Search"
DISTANCE_THRESHOLD = 0.1  # Define the distance threshold (0.1 for "inside" the location)

# Function to make the API request
def get_merchants_data(api_url, location):
    try:
        response = requests.get(f"{api_url}?campaignCode=&location={location}")
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        # Log the error and return an empty response
        print(f"An error occurred while fetching data: {e}")
        return {"merchants": []}  # Fallback to an empty response

# Function to filter and extract the required data for a single location
def extract_single_reward_data(merchants):
    for merchant in merchants:
        # Only process merchants within the distance threshold
        distance = merchant.get("distance", float('inf'))
        if isinstance(distance, (int, float)) and distance <= DISTANCE_THRESHOLD:
            # Extract multiplier values safely
            benefits = merchant.get("benefits", [])
            if benefits:
                multiplier = max([int(benefit.get('value', 0)) for benefit in benefits])
            else:
                multiplier = 0

            # Extract location types (e.g., restaurant, service)
            locations = [merchant.get('type', 'Unknown')]

            # Return the extracted data as JSON
            return {
                "multiplier": str(multiplier),
                "locations": locations
            }
    return None
