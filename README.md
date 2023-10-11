app following this code

https://manage.auth0.com/dashboard/eu/dev-3plxln1pojghexo8/applications/OY99qQHHFr20yepbcXGobi4OgRVe4QxZ/quickstart


Replace <YOUR_SECRET_KEY> with a secret key for your Flask application. You can generate one using the following command:


bash
 
#  run this on your terminal:


openssl rand -hex 32



# AWARD FORCE SSO

https://support.awardforce.com/hc/en-us/articles/4409757409167-3rd-party-authentication


# Get user by email

https://apidocs.awardforce.com/#c53f821a-dccf-4598-ac4b-3efa97a9f00b


# Get user by slug

https://apidocs.awardforce.com/#50a5e897-d50b-4cb8-b60b-68baa373b116

# Get auth token

https://apidocs.awardforce.com/#ce84f46c-ffcd-4791-baf0-9d93cf007288


# steps are

provide the email this will generate the slug

with the slug I will get auth token.

Constructed URL: https://api.cr4ce.com/user/SLUG/auth-token
Authentication Token: auth-token-generated

with the token I will redirect to the login page 
sign_in_url = f"https://{account_domain}/login?token={token}"
