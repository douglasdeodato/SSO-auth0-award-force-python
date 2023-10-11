import json
import os
from os import environ as env
from urllib.parse import quote_plus, urlencode
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from authlib.integrations.flask_client import OAuth
import requests

# Load environment variables from .env
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

# Configure Authlib
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token

    # Automatically fetch JSON data upon successful login
    fetch_json_data()

    return redirect("/")

# Function to fetch JSON data
def fetch_json_data():
    user_info = session.get("user")
    user_email = user_info.get("userinfo", {}).get("email")

    if user_email:
        # Define the API endpoint URL using the email
        api_url = f"https://api.cr4ce.com/user/{user_email}"  # Replace with your API URL

        headers = {
            'Accept': 'application/vnd.Creative Force.v2.1+json',
            'x-api-key': env.get("API_KEY")  # Replace with your API key environment variable
        }

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            
            # Define the filename for the JSON file inside the 'get-user-by-email' folder
            json_directory = os.path.join(os.path.dirname(__file__), 'get-user-by-email')
            json_filename = os.path.join(json_directory, 'output.json')
            
            # Create the directory if it doesn't exist
            os.makedirs(json_directory, exist_ok=True)

            # Add error handling for writing the JSON file
            try:
                with open(json_filename, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                print(f"JSON data has been saved to {json_filename}")
            except Exception as e:
                print(f"Error writing JSON file: {str(e)}")
        else:
            print(f"Request failed with status code: {response.status_code}")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def home():
    user_info = session.get("user")
    
    if user_info is not None:
        user_email = user_info.get("userinfo", {}).get("email")
        return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4), user_email=user_email)
    else:
        return """User is not authenticated. Please log in.
        <a href="/login">Login</a>"""

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=int(env.get("PORT", 3000)))
