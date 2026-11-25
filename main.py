
import os
import logging
from datetime import datetime, timezone

# ==================================
# GOLD AI TRADER - CONFIGURATION
# ==================================

BOT_NAME = "GOLD AI TRADER"
BROKER = "XM"

# Markets to scan
FOREX_PAIRS = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "GBPJPY",
    "EURJPY",
    "AUDUSD",
    "USDCAD",
    "USDCHF",
    "NZDUSD",
    "EURGBP",
    "GBPAUD",
    "GBPCHF",
    "AUDJPY",
    "EURAUD",
    "GBPCAD",
]

# Always include gold against the euro
SPECIAL_MARKETS = ["XAUEUR"]

ALL_MARKETS = FOREX_PAIRS + SPECIAL_MARKETS

# Timeframes for market analysis
TIMEFRAMES = ["4H", "1H", "15M", "5M"]

# Daily signal limits
MAX_DAILY_SIGNALS = 2

# Risk management settings
RISK_PER_TRADE = 0.01
MINIMUM_RISK_REWARD = 2.0

# Minimum setup quality
MINIMUM_SETUP_SCORE = 80

# Telegram configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(BOT_NAME)


def show_configuration():
    logger.info("=" * 40)
    logger.info(BOT_NAME)
    logger.info("=" * 40)
    logger.info("Broker: %s", BROKER)
    logger.info("Markets configured: %s", len(ALL_MARKETS))
    logger.info("Forex pairs: %s", len(FOREX_PAIRS))
    logger.info("Special market: XAUEUR")
    logger.info("Timeframes: %s", TIMEFRAMES)
    logger.info("Maximum daily signals: %s", MAX_DAILY_SIGNALS)
    logger.info("Risk per trade: %s%%", RISK_PER_TRADE * 100)
    logger.info("Minimum risk/reward: 1:%s", MINIMUM_RISK_REWARD)
    logger.info("Minimum setup score: %s", MINIMUM_SETUP_SCORE)
    logger.info("Date: %s", datetime.now(timezone.utc))
    logger.info("=" * 40)


if __name__ == "__main__":
    show_configuration()
