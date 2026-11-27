
import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GOLD AI TRADER")

API_KEY = os.getenv("TWELVE_DATA_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

FOREX_PAIRS = [
    "EUR/USD", "GBP/USD", "USD/JPY",
    "GBP/JPY", "EUR/JPY", "AUD/USD",
    "USD/CAD", "USD/CHF", "NZD/USD",
    "EUR/GBP", "GBP/AUD", "GBP/CHF",
    "AUD/JPY", "EUR/AUD", "GBP/CAD"
]

def get_supported_pairs():
    url = "https://api.twelvedata.com/forex_pairs"

    response = requests.get(
        url,
        params={"apikey": API_KEY},
        timeout=30
    )
    response.raise_for_status()

    data = response.json()

    if data.get("status") != "ok":
        raise RuntimeError(
            data.get("message", "Could not retrieve forex catalogue")
        )

    return {
        item["symbol"].upper()
        for item in data.get("data", [])
    }

def check_gold():
    url = "https://api.twelvedata.com/time_series"

    response = requests.get(
        url,
        params={
            "symbol": "XAU/EUR",
            "interval": "5min",
            "outputsize": 1,
            "apikey": API_KEY
        },
        timeout=30
    )
    response.raise_for_status()
    data = response.json()

    return "values" in data

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        },
        timeout=30
    )
    response.raise_for_status()

def main():
    if not all([API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]):
        raise RuntimeError("One or more GitHub secrets are missing.")

    supported = get_supported_pairs()

    available = []
    unavailable = []

    for pair in FOREX_PAIRS:
        if pair in supported:
            available.append(pair)
        else:
            unavailable.append(pair)

    gold_available = check_gold()

    message = "GOLD AI TRADER - MARKET CHECK\n\n"

    message += "SUPPORTED FOREX PAIRS:\n"
    message += "\n".join(available) if available else "None"

    message += "\n\nUNAVAILABLE FOREX PAIRS:\n"
    message += "\n".join(unavailable) if unavailable else "None"

    message += "\n\nXAUEUR DATA CHECK: "
    message += "AVAILABLE" if gold_available else "UNAVAILABLE"

    message += "\n\nThis is an availability test only. No trades generated."

    send_telegram(message)

    logger.info("Market availability check completed.")

if __name__ == "__main__":
    main()
