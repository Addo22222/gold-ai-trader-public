
import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GOLD AI TRADER")

API_KEY = os.getenv("TWELVE_DATA_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("Telegram credentials are missing.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(
        url,
        json={"chat_id": TELEGRAM_CHAT_ID, "text": message},
        timeout=20
    )
    response.raise_for_status()

def test_market(symbol):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": "5min",
        "outputsize": 5,
        "apikey": API_KEY
    }

    response = requests.get(url, params=params, timeout=20)
    data = response.json()

    if "values" in data:
        return f"{symbol}: Market data connection successful."

    return f"{symbol}: Data unavailable - {data.get('message', 'Unknown error')}"

def main():
    if not API_KEY:
        raise RuntimeError("Twelve Data API key is missing.")

    results = [
        test_market("EUR/USD"),
        test_market("XAU/EUR")
    ]

    message = "GOLD AI TRADER - CONNECTION TEST\n\n"
    message += "\n".join(results)
    message += "\n\nNo trades have been generated."

    send_telegram(message)
    logger.info("Connection test completed.")

if __name__ == "__main__":
    main()

