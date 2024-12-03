import logging
import argparse
from ldap3 import Server, Connection, ALL, NTLM
from Crypto.Hash import MD4

def md4(data):
    """
    Implements MD4 hashing using pycryptodome library.
    """
    hash_obj = MD4.new()
    hash_obj.update(data)
    return hash_obj.digest()

# Ensure MD4 is available globally for NTLM authentication
hashlib.md4 = md4

def enumerate_spns(domain, username, password, dc_ip):
    """
    Enumerates SPNs in the Active Directory domain using LDAP queries.

    Args:
        domain (str): The AD domain (e.g., "example.com").
        username (str): The username to authenticate with.
        password (str): The password for the account.
        dc_ip (str): The IP address of the Domain Controller.
    """
    try:
        # Connect to the LDAP server
        server = Server(dc_ip, get_info=ALL)
        conn = Connection(server, user=f"{domain}\\{username}", password=password, authentication=NTLM)

        if not conn.bind():
            print("[-] Failed to bind to the LDAP server. Check your credentials.")
            return

        print("[+] Connected to the LDAP server.")
        
        # Search for objects with the servicePrincipalName attribute
        search_filter = "(servicePrincipalName=*)"
        attributes = ['servicePrincipalName', 'sAMAccountName', 'distinguishedName']
        conn.search(search_base=f"DC={domain.replace('.', ',DC=')}", search_filter=search_filter, attributes=attributes)

        # Display the results
        print("[*] Enumerating SPNs...")
        for entry in conn.entries:
            account_name = entry.sAMAccountName.value
            dn = entry.distinguishedName.value
            spns = entry.servicePrincipalName.values if entry.servicePrincipalName else []
            
            print(f"\nAccount: {account_name}")
            print(f"Distinguished Name: {dn}")
            print("SPNs:")
            for spn in spns:
                print(f"    {spn}")
        
        conn.unbind()
    except Exception as e:
        print(f"[-] An error occurred: {e}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Enumerate SPNs in an Active Directory domain using LDAP.")
    parser.add_argument("domain", help="The Active Directory domain (e.g., 'example.com')")
    parser.add_argument("username", help="The username for NTLM authentication")
    parser.add_argument("password", help="The password for NTLM authentication")
    parser.add_argument("dc_ip", help="The IP address of the Domain Controller")

    # Parse command line arguments
    args = parser.parse_args()

    # Run the SPN enumeration with the provided arguments
    enumerate_spns(args.domain, args.username, args.password, args.dc_ip)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)  # Set logging to debug for verbose output
    main()
