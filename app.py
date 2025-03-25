from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# LinkedIn OAuth credentials
CLIENT_ID = "864d7i1iuc1uqj"  # Replace with your LinkedIn App Client ID
CLIENT_SECRET = "WPL_AP1.6qT8U8pRwP3YW5yU.OZcXzA=="  # Replace with your LinkedIn App Client Secret
REDIRECT_URI = "https://linkedin-auth-j9im.onrender.com/callback"  # Update this after deployment

# Variables to hold tokens
authorization_code = None
access_token = None


@app.route("/")
def home():
    return '<a href="/login">Login with LinkedIn</a>'


@app.route("/login")
def login():
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope=r_liteprofile%20r_emailaddress%20w_member_social&"
        f"state=RANDOM_STRING"
    )
    return redirect(auth_url)


@app.route("/callback")
def callback():
    global authorization_code, access_token
    code = request.args.get("code")

    if code:
        authorization_code = code
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        params = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        response = requests.post(token_url, data=params)
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            return f"<h1>Access Token: {access_token}</h1>"
        else:
            return f"<h1>Error: {response.json()}</h1>"
    else:
        return "<h1>Error! No authorization code received.</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
