import ipaddress

class Router:
    RIB = []
    FIB = []

    def __init__(self, hostname):
        self.hostname = hostname
        print(f"Router {self.hostname} is booting...")

    def add_route(self, network, prefix_length, next_hop):
        new_route = {
            "network": network,
            "prefix_length": prefix_length,
            "next_hop": next_hop
        }
        self.RIB.append(new_route)
        self.calculate_fib()
    
    def calculate_fib(self):
        print(f"💭 Calculating FIB for router {self.hostname}")
        print("  ❌ Clearing existing FIB")
        self.FIB = []
        for route in self.RIB:
            new_fib_entry = {
                "prefix": ipaddress.IPv4Network(f"{route['network']}/{route['prefix_length']}"),
                "next_hop": ipaddress.IPv4Address(route['next_hop'])
            }
            print(f"  ⚙️ Populating FIB entry: {new_fib_entry}")
    
    def show_ip_route(self):
        sh_ip_route_banner = """ 
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
    D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
    N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
    E1 - OSPF external type 1, E2 - OSPF external type 2

        """
        print(sh_ip_route_banner)
        for route in self.RIB:
            print(f"S     {route['network']}/{route['prefix_length']} via {route['next_hop']}")

corerouter = Router('core-01')

corerouter.add_route("10.10.10.0", 24, "10.0.0.1")
corerouter.add_route("10.10.100.0", 23, '10.0.0.5')
corerouter.add_route("10.100.8.0", 22, "10.0.0.9")
corerouter.add_route("100.10.0.0", 18, "10.0.0.13")

corerouter.show_ip_route()