import hashlib
import json
import requests
from datetime import datetime


def hash_string(input_string: str) -> str:
    return hashlib.sha256(input_string.encode()).hexdigest()


def fetch_json(url: str) -> dict:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return {}


def timestamp_now() -> str:
    return datetime.utcnow().isoformat() + 'Z'


def format_crypto_data(data: dict) -> str:
    return json.dumps(data, indent=4)


def validate_address(address: str) -> bool:
    if len(address) != 42 or not address.startswith('0x'):
        return False
    return all(c in '0123456789abcdefABCDEF' for c in address[2:])


def load_json_file(filepath: str) -> dict:
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filepath}: {e}")
        return {}