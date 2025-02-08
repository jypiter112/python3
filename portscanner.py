import pyfiglet
import sys
import socket
import concurrent.futures
from datetime import datetime

banner = pyfiglet.figlet_format("Port Scanner")
print(banner)

if len(sys.argv) > 2:
    # Hostname to IPv4
    target = socket.gethostbyname(sys.argv[1])
    mode = sys.argv[2]
else:
    print("Usage scan.py <target> <mode> <save on exit (opt)>")
    print("Ex: scan.py scanme.nmap.org q s")
    print("Save: s (4th arg just exists)")
    print("Default mode: q")
    print("Modes: a   - all ports\n\t q - quiet, only common ports")

print("-"*50)
print("Target",target)
print("Mode:", mode)
print("Scan started at "+str(datetime.now()))
print("-"*50)

common_ports = {
    20: "FTP Data Transfer - Used for transferring files in active mode.",
    21: "FTP Control - Used for FTP commands and authentication.",
    22: "SSH - Secure Shell for remote command-line access and administration.",
    23: "Telnet - Unsecured remote login protocol.",
    25: "SMTP - Simple Mail Transfer Protocol for sending emails.",
    53: "DNS - Domain Name System for resolving domain names to IP addresses.",
    67: "DHCP Server - Assigns IP addresses to clients dynamically.",
    68: "DHCP Client - Used by clients to obtain IP addresses from the DHCP server.",
    69: "TFTP - Trivial File Transfer Protocol, a simple file transfer service.",
    80: "HTTP - HyperText Transfer Protocol for web traffic.",
    110: "POP3 - Post Office Protocol for retrieving emails from a mail server.",
    119: "NNTP - Network News Transfer Protocol for Usenet articles.",
    123: "NTP - Network Time Protocol for clock synchronization.",
    135: "RPC - Remote Procedure Call for inter-process communication.",
    137: "NetBIOS Name Service - Name resolution for Windows networking.",
    138: "NetBIOS Datagram Service - Communication over Windows networks.",
    139: "NetBIOS Session Service - Windows file and printer sharing.",
    143: "IMAP - Internet Message Access Protocol for email retrieval.",
    161: "SNMP - Simple Network Management Protocol for network monitoring.",
    162: "SNMP Trap - Used for sending alerts in SNMP.",
    389: "LDAP - Lightweight Directory Access Protocol for directory services.",
    443: "HTTPS - Secure HTTP with encryption via TLS/SSL.",
    445: "SMB - Server Message Block for Windows file sharing.",
    514: "Syslog - Logging service for system messages.",
    587: "SMTP (Secure) - Secure email submission with authentication.",
    631: "IPP - Internet Printing Protocol for remote printing.",
    993: "IMAP (Secure) - IMAP over SSL/TLS for secure email retrieval.",
    995: "POP3 (Secure) - POP3 over SSL/TLS for secure email access.",
    1433: "MSSQL - Microsoft SQL Server database communication.",
    1521: "Oracle SQL - Oracle Database listener.",
    1723: "PPTP - Point-to-Point Tunneling Protocol for VPNs.",
    3306: "MySQL - MySQL database communication.",
    3389: "RDP - Remote Desktop Protocol for Windows remote access.",
    5060: "SIP - Session Initiation Protocol for VoIP signaling.",
    5432: "PostgreSQL - PostgreSQL database communication.",
    5900: "VNC - Virtual Network Computing for remote desktop access.",
    6379: "Redis - In-memory key-value store for caching.",
    8080: "HTTP Alternate - Often used for web services or proxies.",
    8443: "HTTPS Alternate - Secure web traffic over SSL/TLS.",
}


def scan_port(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            res = s.connect_ex((target, port))
            if res == 0:
                desc = common_ports.get(port, "Unknown Service")
                res = f"Port: {port} - OPEN  : {desc}"
                print(res)
                return res
    except socket.gaierror:
        print("Error Invalid host")
        return None
    except socket.timeout:
        print("Error Timeout")
        return None
    except Exception as e:
        print("Error scanning.")
    return None

open_ports = []
try:
    if sys.argv[2] == "a":
        print("Scanning all ports")
        ports = [i for i in range(1, 65536)]
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as exec:
                results = exec.map(scan_port, ports)
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            sys.exit()
        print(f"Scan finished at {datetime.now()}") 
        open_ports = [r for r in results if r is not None]
    else:
        print("Quiet scan")
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as exec:
                results = exec.map(scan_port, common_ports.keys())
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            sys.exit()
        print(f"Scan finished at {datetime.now()}")
        open_ports = [r for r in results if r is not None]

except KeyboardInterrupt:
    print("Keyboard interrupt")
except socket.gaierror:
    print("Hostname resolve failed")
    sys.exit()
except socket.error:
    print("Server not responding")
    sys.exit()
