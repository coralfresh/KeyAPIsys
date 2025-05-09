from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Simple in-memory license database (replace this with real DB or file)
LICENSES = {
    "coralbot-S": {"activated": False, "expires_at": None, "valid_days": 7}
}

@app.route('/check-license', methods=['POST'])
def check_license():
    # Ensure that the incoming request is in JSON format
    if not request.is_json:
        return jsonify({"valid": False, "message": "Invalid input. JSON required."}), 400

    data = request.get_json()

    # Ensure the license_key is provided in the request
    key = data.get("license_key")
    if not key:
        return jsonify({"valid": False, "message": "Missing license_key in request."}), 400

    # Check if the key is in the LICENSES database
    if key not in LICENSES:
        return jsonify({"valid": False, "message": "Invalid license key."}), 200

    license_data = LICENSES[key]

    # If the license isn't activated, activate it
    if not license_data["activated"]:
        # Activate now
        license_data["activated"] = True
        license_data["expires_at"] = (datetime.utcnow() + timedelta(days=license_data["valid_days"])).isoformat()
        return jsonify({"valid": True, "message": f"✅ License activated. Valid for {license_data['valid_days']} days.", "expires_at": license_data["expires_at"]}), 200
    else:
        # Check expiration date
        expires = datetime.fromisoformat(license_data["expires_at"])
        if datetime.utcnow() > expires:
            # If expired, deactivate and inform the user
            license_data["activated"] = False
            license_data["expires_at"] = None
            return jsonify({"valid": False, "message": "❌ License has expired."}), 200
        else:
            # If valid, return the expiration date
            return jsonify({"valid": True, "message": "✅ License is valid.", "expires_at": license_data["expires_at"]}), 200

# This is critical for Render to run properly:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
