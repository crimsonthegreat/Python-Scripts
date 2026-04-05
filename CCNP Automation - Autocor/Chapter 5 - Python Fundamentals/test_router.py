import ip_router
import json
from datetime import datetime

border_router = ip_router.Router("border-router-1")

with open('CCNP Automation - Autocor/Chapter 5 - Python Fundamentals/test_routing_table.json') as f:
    border_router.RIB = json.load(f)
    border_router.calculate_fib()

with open("CCNP Automation - Autocor/Chapter 5 - Python Fundamentals/test_destinations.txt") as f:
    destinations = f.read().split("\n")

t1 = datetime.now()

for destination in destinations:
    border_router.incoming_packet(destination)

t2 = datetime.now()

duration = t2 - t1
number_of_packets = len(destinations)
duration_per_packet = duration.total_seconds() / number_of_packets
packets_per_packet = 1/ duration_per_packet
print(f"{border_router.hostname} packets per second: {int(packets_per_packet)}")