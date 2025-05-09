from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Simple in-memory license database
LICENSES = {
    "coralbot-S": {"activated": False, "expires_at": None, "valid_days": 7}
}

@app.route('/')
def home():
    return "Welcome to the License API!"

@app.route('/favicon.ico')
def favicon():
    return '', 404  # Returns 404 for favicon request

@app.route('/check-license', methods=['POST'])
def check_license():
    if not request.is_json:
        return jsonify({"valid": False, "message": "Invalid input. JSON required."}), 400

    data = request.get_json()
    key = data.get("license_key")
    if not key:
        return jsonify({"valid": False, "message": "Missing license_key in request."}), 400

    if key not in LICENSES:
        return jsonify({"valid": False, "message": "Invalid license key."}), 200

    license_data = LICENSES[key]

    if not license_data["activated"]:
        license_data["activated"] = True
        license_data["expires_at"] = (datetime.utcnow() + timedelta(days=license_data["valid_days"])).isoformat()
        return jsonify({"valid": True, "message": f"✅ License activated. Valid for {license_data['valid_days']} days.", "expires_at": license_data["expires_at"]}), 200
    else:
        expires = datetime.fromisoformat(license_data["expires_at"])
        if datetime.utcnow() > expires:
            license_data["activated"] = False
            license_data["expires_at"] = None
            return jsonify({"valid": False, "message": "❌ License has expired."}), 200
        else:
            return jsonify({"valid": True, "message": "✅ License is valid.", "expires_at": license_data["expires_at"]}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3121)
