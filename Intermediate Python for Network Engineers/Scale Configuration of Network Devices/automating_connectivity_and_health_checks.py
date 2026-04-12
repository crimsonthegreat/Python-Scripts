import socket
import subprocess
from genie.testbed import load

testbed = load("testbed.yaml")
device = testbed.devices['IOL_Router_1']

def check_tcp_connection(host, port):
    try:
        socket.create_connection((host, port), timeout=3)
        print(f"{host}:{port} is reachable")
    except socket.error:
        print(f"Cannot reach {host}:{port}")

def ping_host(host):
    result = subprocess.run(["ping", "-c", "3", host], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{host} is reachable")
    else:
        print(f"{host} is not reachable")

check_tcp_connection("8.8.8.8", 53)
ping_host("8.8.8.8")

check_tcp_connection("10.117.44.153", 22)
ping_host("10.117.44.153")

check_tcp_connection("10.117.44.154", 22)
ping_host("10.117.44.154")

with device as dev:
    output = dev.execute('ping 8.8.8.8')
    print(output)

    if "Seccess rate is 100" in output:
        print("Ping successful")
    else:
        print("Ping may have failed")