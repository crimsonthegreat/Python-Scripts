from genie.testbed import load
import pprint

# Load testbed and connect to device
testbed = load('testbed.yaml')
device = testbed.devices['IOL_Router_1']

try:
    device.connect()
    parsed_output = device.parse('show ip interface brief')
    pprint.pprint(parsed_output)

    interfaces = parsed_output.get('interface', {})
    intf = interfaces.get('Ethernet0/0', {})
    print(intf)
    print(intf.get('status'))
    print(intf.get('protocol'))
    if intf.get('status')  == 'up' and intf.get('protocol') == 'up':
        print("Interface is up and operational")
    else:
        print("Interface is down or has issues")
        
finally:
    device.disconnect()

