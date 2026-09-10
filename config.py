import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
BASE_DIR=Path(__file__).resolve().parent.parent
DATA_FILE=BASE_DIR/"data"/"business_data.xlsx"
OUTPUT_DIR=BASE_DIR/"output"; OUTPUT_DIR.mkdir(exist_ok=True)
EMAIL_SENDER=os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER=os.getenv("EMAIL_RECEIVER")
THRESHOLD=20
