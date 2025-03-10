#!/usr/bin/env python3
"""
Run script for SonicSentinel
Starts the Flask server and initializes all components
"""

from integration import app
from sonicsentinel_ai import SonicSentinelAI
import os
from flask import jsonify, request

# Initialize the AI
ai = SonicSentinelAI()

# @app.route('/api/risk-assessment', methods=['GET'])
# def get_risk_assessment():
#     """Get the current risk assessment"""
#     risk_assessment = ai.calculate_risk_score()
#     return jsonify(risk_assessment)

@app.route('/api/simulate-protection', methods=['POST'])
def simulate_protection():
    """Simulate protection actions for vaults"""
    vaults = request.json.get('vaults', [])
    risk_score = request.json.get('risk_score', 0)
    
    protection_actions = ai.simulate_protection_actions(vaults, risk_score)
    return jsonify(protection_actions)

if __name__ == "__main__":
    # Check if port is specified in environment
    port = int(os.getenv("PORT", 5000))
    
    print(f"Starting SonicSentinel on port {port}")
    print(f"Access the interface at: http://127.0.0.1:{port}")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=port)  # Changed host to 0.0.0.0 to allow all connections