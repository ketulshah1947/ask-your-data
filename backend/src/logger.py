import logging
import sys

logging.basicConfig(
    level=logging.INFO,  # Show info and above (info, warning, error)
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout  # Output to console (stdout)
)
logger = logging.getLogger("ask-your-data")
