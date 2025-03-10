"""
Integration module for Sonic Sentinel AI with the DeFi Timelock Wallet
This module handles the connection between the wallet interface and the AI risk assessment system
"""

import json
from flask import Flask, request, jsonify
from web3 import Web3
from flask import send_from_directory
import os
from datetime import datetime, timedelta

# Import the SonicSentinelAI class
from sonic_sentinel.backend.risk_assessment import SonicSentinelAI
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}) 


# Initialize AI
sentinel_ai = SonicSentinelAI()

# Load environment variables
def load_config():
    """Load configuration from environment or config file"""
    config = {
        "infura_url": os.getenv("INFURA_URL", ""),
        "contract_address": os.getenv("CONTRACT_ADDRESS", ""),
        "private_key": os.getenv("PRIVATE_KEY", ""),
        "chain_id": int(os.getenv("CHAIN_ID", "1"))  # Default to Ethereum mainnet
    }
    
    # Validate config
    for key, value in config.items():
        if not value and key != "private_key":  # private_key can be empty for read-only operations
            print(f"Warning: {key} not set in environment variables")
    
    return config

# Connect to blockchain
def connect_web3(infura_url):
    """Establish connection to Ethereum node"""
    web3 = Web3(Web3.HTTPProvider(infura_url))
    if not web3.is_connected():
        print("Failed to connect to Ethereum node")
        return None
    print(f"Connected to Ethereum node. Current block: {web3.eth.block_number}")
    return web3

# Load contract ABI
def load_contract_abi():
    """Load the contract ABI from JSON file"""
    try:
        with open("contract_abi.json", "r") as abi_file:
            contract_abi = json.load(abi_file)
        return contract_abi
    except FileNotFoundError:
        print("Error: contract_abi.json not found")
        return None

# API endpoint for risk assessment
@app.route('/api/risk-assessment', methods=['GET', 'POST'])
def assess_risk():
    """API endpoint to perform risk assessment on a wallet transaction"""
    if request.method == 'GET':
        # Get current market and social data
        market_data = sentinel_ai.load_market_data()
        social_signals = sentinel_ai.load_social_signals()
        
        # Calculate risk score
        risk_score = sentinel_ai.calculate_risk_score()
        
        # Determine if this transaction needs protection
        needs_protection = risk_score > sentinel_ai.risk_threshold
        
        # Prepare response
        response = {
            'risk_score': risk_score,
            'market_data': market_data,
            'social_signals': social_signals,
            'needs_protection': needs_protection,
            'recommendation': "Consider enabling timelock" if needs_protection else "Standard transaction ok",
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    else:  # POST
        data = request.json

# API endpoint for extending timelock
@app.route('/api/extend_timelock', methods=['POST'])
def extend_timelock():
    """API endpoint to extend the timelock period for a vault"""
    config = load_config()
    web3 = connect_web3(config["infura_url"])
    contract_abi = load_contract_abi()
    
    if not web3 or not contract_abi:
        return jsonify({"error": "Failed to initialize blockchain connection"}), 500
    
    data = request.json
    vault_id = data.get('vault_id')
    additional_days = data.get('additional_days', 0)
    
    if not vault_id:
        return jsonify({"error": "Missing vault_id parameter"}), 400
    
    try:
        # Create contract instance
        contract = web3.eth.contract(address=config["contract_address"], abi=contract_abi)
        
        # Create account from private key
        account = web3.eth.account.from_key(config["private_key"])
        
        # Build transaction
        transaction = contract.functions.extendUnlockTime(
            vault_id,
            int(additional_days)
        ).build_transaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
            'chainId': config["chain_id"]
        })
        
        # Sign and send transaction
        signed_txn = web3.eth.account.sign_transaction(transaction, config["private_key"])
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        return jsonify({
            "success": True,
            "transaction_hash": web3.to_hex(tx_hash),
            "message": f"Extended timelock for vault {vault_id} by {additional_days} days"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Add route to serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('sonic_sentinel/frontend', 'index.html')

# Serve static files
@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(f"sonic_sentinel/frontend/{path}"):
        return send_from_directory('sonic_sentinel/frontend', path)
    return "Not found", 404


@app.route('/api/wallet_data', methods=['POST'])
def get_wallet_data():
    """API endpoint to get wallet data"""
    data = request.json
    wallet_address = data.get('address')
    
    if not wallet_address:
        return jsonify({"error": "Missing wallet address"}), 400
    
    # For demo purposes, return mock data
    # In production, you would query your blockchain/contract
    return jsonify({
        "address": wallet_address,
        "balance": 2500,
        "protected": 1250,
        "vaults": [
            {
                "id": 1,
                "amount": 1000,
                "unlock_days": 12,
                "status": "Protected"
            },
            {
                "id": 2,
                "amount": 250,
                "unlock_days": 5,
                "status": "Protected"
            }
        ]
    })

# Mock wallet connection for testing/development
@app.route('/api/mock_wallet', methods=['POST'])
def mock_wallet_connection():
    """Provides a mock wallet connection for testing without a real wallet"""
    return jsonify({
        "connected": True,
        "address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",  # Example address
        "network": "Ethereum Testnet",
        "balance": "10.5 ETH"
    })

# Main entry point
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)