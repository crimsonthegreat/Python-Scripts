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

"""
If you are taking IPYNE on Cisco U and following along, their code does not work and will return errors.
The above code works and is tested against a virtual router in CML.  The with portion of the Cisco U code returns
error 'TypeError: 'Device' object is not callable' meaning the device is not able to be used as a context object
and instead needs to be a hard coded connect and disconnect.
Additionally, the intf section does not work because the parse stores all of the interfaces under the key interface,
which has to be pulled first and then you can get the specific interface info you are looking for.
"""