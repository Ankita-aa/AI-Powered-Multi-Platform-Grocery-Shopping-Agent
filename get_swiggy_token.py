import base64
import hashlib
import os
import secrets
import urllib.parse
import webbrowser
import requests

SWIGGY_BASE = "https://mcp.swiggy.com"
REDIRECT_URI = "http://localhost:8000/callback"


def generate_pkce():
    code_verifier = secrets.token_urlsafe(64)
    hashed = hashlib.sha256(code_verifier.encode("ascii")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(hashed).decode("ascii").rstrip("=")
    )
    return code_verifier, code_challenge


def get_token():
    code_verifier, code_challenge = generate_pkce()

    # Step 1: Build Authorization URL
    params = {
        "response_type": "code",
        "client_id": "localhost_client",
        "redirect_uri": REDIRECT_URI,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "scope": "mcp:tools mcp:resources mcp:prompts",
    }
    auth_url = f"{SWIGGY_BASE}/auth/authorize?{urllib.parse.urlencode(params)}"

    print("Opening browser for Swiggy Phone + OTP authentication...")
    print(f"URL: {auth_url}")
    webbrowser.open(auth_url)

    # Step 2: Paste the redirected callback URL or authorization code here
    redirected_url = input(
        "\nAfter completing OTP in browser, paste the FULL redirected URL from your browser address bar here: "
    )

    parsed_url = urllib.parse.urlparse(redirected_url.strip())
    query_params = urllib.parse.parse_qs(parsed_url.query)
    auth_code = query_params.get("code", [None])[0]

    if not auth_code:
        print("Failed to parse authorization code!")
        return

    # Step 3: Exchange Authorization Code for Access Token
    token_url = f"{SWIGGY_BASE}/auth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "code_verifier": code_verifier,
        "redirect_uri": REDIRECT_URI,
    }

    res = requests.post(token_url, json=payload)
    if res.status_code == 200:
        data = res.json()
        print("\n Successfully Authenticated!")
        print(f"Access Token: {data['access_token']}")
        print(f"Token Expires In: {data.get('expires_in')} seconds (5 Days)")

        # Save to .env
        with open(".env", "a") as f:
            f.write(f"\nSWIGGY_ACCESS_TOKEN={data['access_token']}\n")
        print("Saved SWIGGY_ACCESS_TOKEN to .env!")
    else:
        print("Failed to fetch token:", res.text)


if __name__ == "__main__":
    get_token()