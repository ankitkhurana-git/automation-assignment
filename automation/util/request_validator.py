def validate_request(data):
    if {"interface-name", "shutdown", "device-name", "ip-address"}.issubset(data.keys()):
        return True
    else:
        return False
