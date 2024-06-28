import logging
import os
import secrets

from dotenv import load_dotenv
from flask import Flask, render_template_string, redirect, request, session
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from requests import get

load_dotenv()

class QuickbookClient:
    def __init__(self):
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        redirect_uri = os.getenv("REDIRECT_URI")
        environment = os.getenv("ENVIRONMENT")
        self.base_url = os.getenv("BASE_URL")

        self.realm_id = None
        self.scopes = [Scopes.ACCOUNTING]

        self.auth_client = AuthClient(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            environment=environment
        )

    def get_auth_url(self):
        return self.auth_client.get_authorization_url(self.scopes)

    def set_access_token(self, auth_code, realmId):
        self.auth_client.get_bearer_token(auth_code=auth_code, realm_id=realmId)

    def request_helper(self, url_part, method="get"):
        final_url = self.base_url + url_part
        headers = {
            "Authorization": f"Bearer {self.auth_client.access_token}",
            "Accept": "application/json"
        }

        data = {}
        if method == "get":
            response = get(final_url, headers=headers)
            if response.ok:
                data = response.json()

        return data

    def get_company_info(self):
        return self.request_helper(f"/v3/company/{self.auth_client.realm_id}/companyinfo/{self.auth_client.realm_id}")

app = Flask(__name__)

app.secret_key = secrets.token_urlsafe(32)

# Setup logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return render_template_string('''
        <html>
            <body>
                <form action="{{ url_for('get_url') }}" method="get">
                    <button type="submit">Click me</button>
                </form>
            </body>
        </html>
    ''')

@app.route('/get-url', methods=['GET'])
def get_url():
    client = QuickbookClient()
    url = client.get_auth_url()
    return redirect(url)

@app.route('/callback', methods=['GET'])
def callback():
    query_params = request.args
    client = QuickbookClient()

    code = query_params.get("code", None)
    state = query_params.get("state", None)
    realmId = query_params.get("realmId", None)

    if code and realmId:
        client.set_access_token(code, realmId)

    company_info = client.get_company_info()
    print("company_info", company_info)

    return f"Query parameters logged: {query_params}", 200

if __name__ == '__main__':
    app.run(debug=True)
