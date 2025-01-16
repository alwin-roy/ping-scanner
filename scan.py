from ping3 import ping, verbose_ping
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import pyfiglet

def domain_scan():
    inp_domain = input("Enter the domain/ip address (eg: www.example.com / 1.1.1.1): ")
    try:
        pinging = ping(inp_domain, timeout=1)
        if pinging is not None:
            print("Host is live")

    except Exception as e:
        print(f"Error occurred while pinging {inp_domain}: {e}")

def sort_ips(ip_list):
    return sorted(ip_list, key=lambda ip: tuple(map(int, ip.split('.'))))

def network_scan():
    inp_ip = input("Enter the IP address (e.g., 192.168.1.0): ")
    split_ip = inp_ip.split(".")
    ip_addr = f"{split_ip[0]}.{split_ip[1]}.{split_ip[2]}."

    start_ip = int(input("Enter the start IP (e.g., 1): "))
    end_ip = int(input("Enter the end IP (e.g., 254): ")) + 1

    start_time = datetime.now()

    result = []

    def scan_ip(ipp):
        """Function to ping a single IP."""
        addr = f"{ip_addr}{ipp}"
        try:
            pinging = ping(addr, timeout=1)
            # Only return the IP if ping is successful (ping > 0 means success)
            if pinging is not None and pinging > 0:
                return addr
        except Exception as e:
            print(f"Error occurred while pinging {addr}: {e}")
        return None  # Return None if not live

    # Number of threads in the thread pool
    num_threads = 50

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks to the thread pool
        future_to_ip = {executor.submit(scan_ip, ipp): ipp for ipp in range(start_ip, end_ip)}

        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                result_ip = future.result()
                if result_ip:
                    result.append(result_ip)
            except Exception as e:
                print(f"Error occurred for IP {ip}: {e}")

    sorted_result = sort_ips(result)

    if sorted_result:
        for ip in sorted_result:
            print(f"{ip} is Live")
    else:
        print("No live IPs found.")

    finish_time = datetime.now() - start_time
    print(f"Total scanning time: {finish_time.total_seconds()} seconds")

def main():
    x = True

    print(pyfiglet.figlet_format("PING SCANNER", font="slant"))

    while x is True:
        print("1. ping domain")
        print("2. ping network")
        print("3. exit")

        choice = input("Enter the choice (eg: 1): ")

        if choice == "1":
            domain_scan()
        elif choice == "2":
            network_scan()
        elif choice == "3":
            x = False
        else:
            print("Invalid input, Try Again")
        print("*************************************")
        print("\n")

if __name__ == "__main__":
    main()
