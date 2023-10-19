# auth_token_generator.py

import os
import requests
from os import environ as env

def generate_auth_token(session, json_filename):
    user_info = session.get("user")
    user_email = user_info.get("userinfo", {}).get("email")

    if user_email:
        # Read the 'slug' from the JSON file generated by get-user-by-email
        with open(json_filename, 'r') as json_file:
            data = json.load(json_file)
            slug = data.get('slug', '')

        # Construct the API URL using the 'slug'
        api_url_external = f"https://api.cr4ce.com/user/{slug}/auth-token"

        # Define the headers
        headers = {
            'Accept': 'application/vnd.Creative Force.v2.1+json',
            'x-api-key': env.get("API_KEY_EXTERNAL")  # Use the API key from your environment variables
        }

        # Send the GET request
        response = requests.get(api_url_external, headers=headers)

        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Save the authentication token to a JSON file in the 'auth-token' folder
            auth_token_directory = os.path.join(os.path.dirname(__file__), 'auth-token')
            os.makedirs(auth_token_directory, exist_ok=True)

            auth_token_filename = os.path.join(auth_token_directory, 'auth_token.json')

            with open(auth_token_filename, 'w') as auth_token_file:
                json.dump(data, auth_token_file, indent=4)

            print(f"Authentication Token has been saved to {auth_token_filename}")
        else:
            print(f"Request failed with status code: {response.status_code}")