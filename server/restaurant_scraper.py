import requests
import json

# Define API endpoint and parameters
api_url = "https://eataroundtown.marriott.com/api/v2/Merchants/Search"
location = "37.22,-80.42"  # Example user location coordinates

# Make the API request
response = requests.get(f"{api_url}?campaignCode=&location={location}")
data = response.json()  # Parse the JSON response

# Define function to extract the required data
def extract_rewards_data(merchants):
    extracted_data = []
    for merchant in merchants:
        # Extract multiplier values
        multiplier = max([int(benefit['value']) for benefit in merchant['benefits']])

        # Extract location types (e.g., restaurant, service)
        locations = [merchant['type']]

        # Add extracted data to the list
        extracted_data.append({
            "multiplier": str(multiplier),
            "locations": locations
        })

    return extracted_data

# Extract the data from the merchants section
merchants = data.get("merchants", [])
reward_data = extract_rewards_data(merchants)

# Print or process the reward data
print(json.dumps(reward_data, indent=2))
