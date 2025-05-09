from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Simple in-memory license database (for demonstration)
LICENSES = {
    "coralbot-S": {"activated": False, "expires_at": None, "valid_days": 7}
}

@app.route('/check-license', methods=['POST'])
def check_license():
    data = request.get_json()
    key = data.get("license_key")

    if key not in LICENSES:
        return jsonify({"valid": False, "message": "Invalid license key."}), 200

    license_data = LICENSES[key]

    if not license_data["activated"]:
        return jsonify({"valid": True, "message": "License is valid and not yet activated."}), 200
    else:
        expires = datetime.fromisoformat(license_data["expires_at"])
        if datetime.utcnow() > expires:
            return jsonify({"valid": False, "message": "❌ License has expired."}), 200
        else:
            return jsonify({"valid": True, "message": "✅ License is currently active.", "expires_at": license_data["expires_at"]}), 200

@app.route('/activate-license', methods=['POST'])
def activate_license():
    data = request.get_json()
    key = data.get("license_key")

    if key not in LICENSES:
        return jsonify({"valid": False, "message": "Invalid license key."}), 200

    license_data = LICENSES[key]

    if not license_data["activated"]:
        # Activate now
        license_data["activated"] = True
        license_data["expires_at"] = (datetime.utcnow() + timedelta(days=license_data["valid_days"])).isoformat()
        return jsonify({
            "valid": True,
            "message": f"✅ License activated. Valid for {license_data['valid_days']} days.",
            "expires_at": license_data["expires_at"]
        }), 200
    else:
        expires = datetime.fromisoformat(license_data["expires_at"])
        if datetime.utcnow() > expires:
            return jsonify({"valid": False, "message": "❌ License has expired."}), 200
        else:
            return jsonify({
                "valid": True,
                "message": "✅ License is already active.",
                "expires_at": license_data["expires_at"]
            }), 200

# This is critical for Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
