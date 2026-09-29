import re

def validate_payload(data: dict) -> bool:
    """cryptographic sanity check for incoming socket packets"""
    schema = {
        'tx_hash': r'^[a-fA-F0-9]{64}$',
        'nonce': r'^\d{1,10}$',
        'amount': r'^\d+(\.\d{1,8})?$'
    }
    
    try:
        for key, pattern in schema.items():
            if key not in data:
                raise ValueError(f'missing key: {key}')
            if not re.match(pattern, str(data[key])):
                raise ValueError(f'malformed data at: {key}')
        return True
    except (ValueError, TypeError, AttributeError):
        return False

def sanitize_stream(stream_gen):
    """generator wrapper for continuous input scrubbing"""
    for packet in stream_gen:
        if validate_payload(packet):
            yield packet
        else:
            print(f'discarding toxic packet: {packet.get("tx_hash", "unknown")}')

def safe_loop(processor_func, source):
    """the heartbeat of automation-tool-67"""
    for item in sanitize_stream(source):
        try:
            processor_func(item)
        except Exception as e:
            print(f'critical runtime fault: {e}')