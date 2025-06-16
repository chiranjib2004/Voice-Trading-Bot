from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve API key and port from the environment
BLAND_AI_API_KEY = os.getenv("BLAND_AI_API_KEY")
PORT = os.getenv("PORT", 3000)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start-call", methods=["POST"])
def start_call():
    try:
        # Prepare to call bland.ai's endpoint to simulate a voice conversation start.
        bland_api_url = "https://api.bland.ai/v1/calls"
        post_data = {
            "pathway_id": "your_demo_pathway_id",  # Replace with your actual pathway id if available.
            "task": "Initiate OTC order process"
        }
        headers = {
            "Content-Type": "application/json",
            "authorization": BLAND_AI_API_KEY,
        }
        # Send a POST request to bland.ai.
        response = requests.post(bland_api_url, json=post_data, headers=headers)
        # In this simulation, we ignore the response content and directly return a greeting.
        return jsonify({"message": "Welcome! Please select an exchange: OKX, Bybit, Deribit, or Binance."})
    except Exception as e:
        print("Error starting call:", e)
        return jsonify({"message": "Failed to start the conversation."}), 500

@app.route("/select-exchange", methods=["POST"])
def select_exchange():
    data = request.json
    exchange = data.get("exchange", "").strip().lower()

    global available_symbols  # Store symbols globally for voice use
    available_symbols = {}

    try:
        if exchange == "binance":
            binance_info_url = "https://api.binance.com/api/v3/exchangeInfo"
            response = requests.get(binance_info_url)
            response_data = response.json()
            
            # Store ALL symbols dynamically (not just a subset)
            for s in response_data.get('symbols', []):
                available_symbols[s['symbol'].lower()] = s['symbol']

            return jsonify({"message": "Exchange selected: Binance. Now specify **any** valid symbol to trade."})
        else:
            return jsonify({"message": f"Exchange '{exchange}' integration coming soon!"})
    except Exception as e:
        print("Error fetching symbols:", e)
        return jsonify({"message": "Failed to retrieve symbol data. Please try again."}), 500
    
symbol_aliases = {
    "bitcoin": "BTCUSDT",
    "ethereum": "ETHUSDT",
    "dogecoin": "DOGEUSDT",
    "solana": "SOLUSDT",
    "cardano": "ADAUSDT"
}

@app.route("/select-symbol", methods=["POST"])
def select_symbol():
    data = request.json
    spoken_symbol = data.get("symbol", "").strip().lower()
    
    # Check if the spoken symbol is an alias
    symbol = symbol_aliases.get(spoken_symbol, spoken_symbol.upper())

    if symbol in available_symbols.values():  # Verify if it's a valid Binance symbol
        try:
            ticker_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            response = requests.get(ticker_url)
            response_data = response.json()
            price = response_data.get("price", "Unavailable")

            return jsonify({"message": f"The current price of {symbol} is {price}. Please provide the quantity and order price."})
        except Exception as e:
            print("Error fetching ticker price:", e)
            return jsonify({"message": "Failed to retrieve market price, please try again."}), 500
    else:
        return jsonify({"message": f"Symbol '{spoken_symbol}' not recognized. Try again or say Bitcoin, Ethereum, etc."})
    
@app.route("/place-order", methods=["POST"])
def place_order():
    data = request.json
    exchange = data.get("exchange", "")
    symbol = data.get("symbol", "")
    quantity = data.get("quantity", "")
    target_price = data.get("targetPrice", "")
    
    # Simulate confirmation without placing a real order.
    confirmation_msg = f"Order confirmed: Place {quantity} units of {symbol} at {target_price} on {exchange}."
    return jsonify({"message": confirmation_msg})

@app.route("/stop-call", methods=["POST"])
def stop_call():
    return jsonify({"message": "Conversation ended. Thank you for using the bot."})

if __name__ == "__main__":
    app.run(debug=True, port=int(PORT))

@app.route("/select-exchange", methods=["POST"])
def select_exchange():
    data = request.json
    exchange = data.get("exchange", "").strip().lower()

    try:
        if exchange == "binance":
            binance_info_url = "https://api.binance.com/api/v3/exchangeInfo"
            response = requests.get(binance_info_url)
            response_data = response.json()
            symbols = [s['symbol'] for s in response_data.get('symbols', [])]
            symbols_part = ", ".join(symbols[:10])
            message = f"Available symbols on Binance: {symbols_part}. Please state the symbol you wish to trade."
            return jsonify({"message": message})
        else:
            # If the exchange doesn't match exactly as expected
            return jsonify({"message": f"Exchange '{exchange}' integration coming soon!"})
    except Exception as e:
        print("Error fetching symbols:", e)
        return jsonify({"message": "Failed to retrieve symbol data. Please try again."}), 500