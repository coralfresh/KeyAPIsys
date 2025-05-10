from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Simple in-memory license database (for demonstration)
LICENSES = {
    # 1 Month (30 days)
    "coralbot-mlHmL5v3lP": {"activated": False, "expires_at": None, "valid_days": 30},
    "coralbot-7dtZGbYvVs": {"activated": False, "expires_at": None, "valid_days": 30},
    "coralbot-IzzUq3TOU1": {"activated": False, "expires_at": None, "valid_days": 30},
    "coralbot-dH8JJbYEmP": {"activated": False, "expires_at": None, "valid_days": 30},
    "coralbot-atzWXXshJn": {"activated": False, "expires_at": None, "valid_days": 30},

    # 2 Weeks (14 days)
    "coralbot-S0RvYJfaZG": {"activated": False, "expires_at": None, "valid_days": 14},
    "coralbot-EBQvcDSGMS": {"activated": False, "expires_at": None, "valid_days": 14},
    "coralbot-0Py9g33WLa": {"activated": False, "expires_at": None, "valid_days": 14},
    "coralbot-FGMHmG7ZP5": {"activated": False, "expires_at": None, "valid_days": 14},
    "coralbot-5BzRPW144r": {"activated": False, "expires_at": None, "valid_days": 14},

    # 1 Week (7 days)
    "coralbot-JbWHb7N1Tt": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-P7ghRra3Rb": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-3YGNkpPQqC": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-UHKwvJxxed": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-bo69OPqcwl": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-UtHxe0i3rP": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-OSIcTP14Hr": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-YIWb5JDsSF": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-6xrS2ukoTc": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-5wLzuGlqqy": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-sE2HewAJ0f": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-fGjE9Jr0W0": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-YXvt0Zg0GT": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-ExpyMqRDaF": {"activated": False, "expires_at": None, "valid_days": 7},
    "coralbot-tgs0Xg68uz": {"activated": False, "expires_at": None, "valid_days": 7}
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
    port = int(os.environ.get('PORT', 3121))
    app.run(host='0.0.0.0', port=port)
