from flask import Flask, render_template, jsonify, request
import random
import smtplib
from email.message import EmailMessage
import logging
import json
import os
from datetime import datetime
import socket
import time
from web3 import Web3
from dotenv import load_dotenv
import os
load_dotenv()


app = Flask(__name__)

# --- Configuration ---
materials = [
    "PCB_Boards", "Microcontrollers", "Capacitors", "Resistors", 
    "Ethernet_Ports", "LED Indicators", "Aluminum_Casings", 
    "Cooling_Fans", "Power_Supplies", "Plastic_Casings"
]
LOW_STOCK_THRESHOLD = 20
SENDER_EMAIL = "toimoitoi102@gmail.com"
SENDER_PASSWORD = "usjz iidn nfou lluw"
SUPPLIER_EMAIL = "toimoitoi101@gmail.com"

# --- Hedera EVM (MetaMask) Configuration ---
HEDERA_RPC_URL = "https://testnet.hashio.io/api"  # For Hedera Testnet
CONTRACT_ADDRESS = "0x2BC1893457d9Ec5f16925275c83F5E48393Af0d0"  # Replace with your contract's EVM address
CONTRACT_ABI = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "price",
				"type": "uint256"
			}
		],
		"name": "ProductAdded",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "buyer",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "quantity",
				"type": "uint256"
			}
		],
		"name": "ProductPurchased",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_price",
				"type": "uint256"
			}
		],
		"name": "addProduct",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "productId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "quantity",
				"type": "uint256"
			}
		],
		"name": "buyProduct",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "productId",
				"type": "uint256"
			}
		],
		"name": "getProduct",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "buyer",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "productId",
				"type": "uint256"
			}
		],
		"name": "getQuantityBought",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "nextProductId",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "products",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "price",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "exists",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "quantitiesBought",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "productId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "newPrice",
				"type": "uint256"
			}
		],
		"name": "updatePrice",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "withdraw",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(HEDERA_RPC_URL))
if not w3.is_connected():
    raise Exception("Failed to connect to Hedera EVM")

# --- Logging Setup ---
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'time': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'message': record.getMessage()
        }
        return json.dumps(log_record)

logger = logging.getLogger('stock_logger')
handler = logging.FileHandler('stock_alert.jsonlog')
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# --- Backend Functions ---
def simulate_rfid_stock():
    return {material: random.randint(5, 100) for material in materials}

def send_price_request_email(material, quantity):
    price_form_url = f"http://localhost:5000/respond_price?material={material}&id={int(time.time())}"
    
    msg = EmailMessage()
    msg['From'] = SENDER_EMAIL
    msg['To'] = SUPPLIER_EMAIL
    msg['Subject'] = f"Request for Price: {material}"
    msg.set_content(f"""
    Dear Supplier,
    Our stock for {material} is low ({quantity} units remaining).
    Kindly provide the current price per unit using this link:
    {price_form_url}
    Regards,
    Smart Stock System
    """)

    try:
        socket.create_connection(("smtp.gmail.com", 465), timeout=5)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        return True, None
    except Exception as e:
        return False, str(e)

def add_to_blockchain(request_id, name, price_in_hbar):
    try:
        private_key = os.getenv("PRIVATE_KEY")
        account = w3.eth.account.from_key(private_key)
        w3.eth.default_account = account.address

        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
        price_wei = int(price_in_hbar * 10**18)

        tx = contract.functions.addProduct(name, price_wei).build_transaction({
            'chainId': 296,
            'gas': 200000,
            'nonce': w3.eth.get_transaction_count(account.address),
            # Remove gasPrice for now to test
        })

        print("Built TX:")
        import pprint
        pprint.pprint(tx)

        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        print(f"Signed TX type: {type(signed_tx)}")
        print(f"Signed TX fields: {dir(signed_tx)}")

        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction) 


        return True, tx_hash.hex()
    except Exception as e:
        import traceback
        return False, traceback.format_exc()



print(f"Connected to Hedera EVM: {w3.is_connected()}")
print(f"Latest block: {w3.eth.block_number}")
# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('dashboard.html', 
                         LOW_STOCK_THRESHOLD=LOW_STOCK_THRESHOLD,
                         materials=materials)

@app.route('/get_stock')
def get_stock():
    return jsonify(simulate_rfid_stock())

@app.route('/simulate_scan')
def simulate_scan():
    stock = simulate_rfid_stock()
    logger.info("Simulated RFID scan performed")
    return jsonify(stock)

@app.route('/request_supplier', methods=['POST'])
def request_supplier():
    data = request.json
    material = data['material']
    quantity = data['quantity']
    
    success, error = send_price_request_email(material, quantity)
    
    if success:
        logger.info(f"Email alert sent for {material} (low stock: {quantity} units)")
        return jsonify({'success': True})
    else:
        logger.error(f"Failed to send email for {material}: {error}")
        return jsonify({'success': False, 'error': error})

@app.route('/respond_price')
def respond_price():
    material = request.args.get('material')
    request_id = request.args.get('id')
    return render_template('price_form.html', material=material, request_id=request_id)

@app.route('/submit_price', methods=['POST'])
def submit_price():
    material = request.form['material']
    price = float(request.form['price'])
    request_id = request.form['request_id']

    # Save to JSON file (original functionality)
    new_entry = {"request_id": request_id, "material": material, "price": price}
    prices_file = 'prices.json'
    
    if os.path.exists(prices_file):
        with open(prices_file, 'r') as f:
            all_prices = json.load(f)
    else:
        all_prices = []
    
    all_prices.append(new_entry)
    with open(prices_file, 'w') as f:
        json.dump(all_prices, f, indent=4)

    # New blockchain integration
    success, tx_hash = add_to_blockchain(request_id, material, price)
    
    if success:
        logger.info(f"Added to blockchain: {material} (TX: {tx_hash})")
        return f"Price recorded locally and on blockchain! TX Hash: {tx_hash}"
    else:
        logger.error(f"Blockchain error: {tx_hash}")
        return f"Price saved locally but blockchain failed: {tx_hash}"

@app.route('/buy_materials')
def buy_materials():
    try:
        with open('prices.json', 'r') as f:
            price_data = json.load(f)
    except FileNotFoundError:
        price_data = []
    return render_template('buy_materials.html', prices=price_data)

@app.route('/send_test_email')
def send_test_email():
    success, error = send_price_request_email("TEST MATERIAL", 10)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': error})

@app.route('/get_logs')
def get_logs():
    try:
        with open('stock_alert.jsonlog', 'r') as f:
            logs = [json.loads(line) for line in f.readlines()]
        return jsonify(logs[-50:])
    except FileNotFoundError:
        return jsonify([])

if __name__ == '__main__':
    logger.info("Stock Alert System started")
    app.run(debug=True)