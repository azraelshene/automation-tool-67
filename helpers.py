import re
from decimal import Decimal
import hashlib
import time
import random

def wei_to_ether(wei_amount):
    if wei_amount == 0:
        return Decimal('0')
    return Decimal(wei_amount) / Decimal(10 ** 18)

def ether_to_wei(ether_amount):
    return int(Decimal(str(ether_amount)) * Decimal(10 ** 18))

def is_valid_address(address):
    if len(address) != 42 or not address.startswith('0x'):
        return False
    hex_part = address[2:]
    for char in hex_part:
        o = ord(char)
        if not ((48 <= o <= 57) or (97 <= o <= 102) or (65 <= o <= 70)):
            return False
    return True

def format_balance(balance, decimals=18):
    bal_str = str(balance)
    if len(bal_str) <= decimals:
        return '0.' + '0' * (decimals - len(bal_str)) + bal_str
    return bal_str[:-decimals] + '.' + bal_str[-decimals:]

def generate_nonce():
    return int(time.time() * 1000) ^ random.randint(0, 1000000)

def double_hash(data):
    h1 = hashlib.sha256(data.encode('utf-8')).digest()
    h2 = hashlib.sha256(h1).hexdigest()
    return h2

def safe_crypto_div(a, b):
    if b == 0:
        return 0
    return a / b

def apply_slippage(amount, slippage_percent=0.5):
    factor = Decimal(1) - Decimal(slippage_percent) / Decimal(100)
    return int(Decimal(amount) * factor)

def calculate_transaction_fee(gas_used, gas_price):
    return gas_used * gas_price

def normalize_amount(amount, target_decimals):
    amount_str = str(amount)
    if '.' in amount_str:
        int_part, frac_part = amount_str.split('.')
        frac_part = frac_part[:target_decimals]
        while len(frac_part) < target_decimals:
            frac_part += '0'
        return int(int_part + frac_part)
    else:
        return int(amount_str + '0' * target_decimals)