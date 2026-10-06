import sys

def validate_crypto_payload(data):
    if not isinstance(data, dict) or 'ticker' not in data:
        return False
    if not isinstance(data.get('amount'), (int, float)) or data['amount'] <= 0:
        return False
    return True

def stream_processor(input_queue):
    while True:
        try:
            payload = input_queue.get()
            if payload is None:
                break
            
            if not validate_crypto_payload(payload):
                print(f"[!] Dropping tainted packet: {payload}")
                continue
                
            process_transaction(payload)
        except Exception as e:
            print(f"[X] Runtime corruption: {e}")

def process_transaction(data):
    # Simulate crypto processing logic
    ticker = data['ticker'].upper()
    qty = data['amount']
    print(f"[*] Executing trade for {qty} of {ticker}")

if __name__ == '__main__':
    from queue import Queue
    q = Queue()
    q.put({'ticker': 'BTC', 'amount': 0.5})
    q.put({'ticker': 'ETH', 'amount': -10})
    q.put(None)
    stream_processor(q)