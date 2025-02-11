# DOS

![Screenshot](screenshot.png)

Test out internal routers by simulating a Denial of Service (DOS) attack on the network. This is done by sending various types of attack on the host which includes: SYN Flood, UDP Flood, ICMP Flood, and Slowloris.

## Attack Vectors

### SYN Flood  
A SYN Flood is a denial-of-service attack where the attacker sends a rapid succession of TCP SYN requests to a target, overwhelming its ability to handle legitimate connections by filling the connection queue.  

### UDP Flood  
A UDP Flood overwhelms a target by flooding it with User Datagram Protocol (UDP) packets on random ports, forcing the device to process malformed or unresolvable requests and exhausting its resources.  

### ICMP Flood  
An ICMP Flood (or "Ping Flood") bombards a target with excessive ICMP echo-request (ping) packets, aiming to saturate bandwidth or overload the device’s capacity to respond.  

### Slowloris  
Slowloris is a low-bandwidth DDoS attack that opens multiple partial HTTP connections to a target and keeps them open indefinitely, exhausting the server’s concurrent connection pool.  

### UPnP Abuse  
UPnP Abuse exploits Universal Plug and Play (UPnP) protocols to trick routers into opening unauthorized ports or forwarding traffic, potentially exposing internal networks to external attacks.  

### Credential Stuffing  
Credential Stuffing automates login attempts using common default credentials (e.g., `admin:admin`) to gain unauthorized access to router admin interfaces or services.


## Disclaimer
This tool is for educational purposes only. The author will not be responsible for any misuse of this tool.