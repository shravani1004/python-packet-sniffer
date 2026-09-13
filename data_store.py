packets = []

def add_packet(data):
    packets.append(data)

def get_packets():
    return packets[-100:]  # last 100 packets