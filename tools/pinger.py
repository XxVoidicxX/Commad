# ==================================================
# Secton: Pinger

import socket
import subprocess
import time
import platform
from ping3 import ping

class Pinger:
    def __init__(self, authenticated=True):
        self.authenticated = authenticated

    def tool_menu_networking_ip_pinger(self):
        if not self.authenticated:
            self.failed_auth()
            return

        print()
        time.sleep(0.5)
        print(" [ COMMAND PINGER: Enter an IP address or domain name to ping ")
        print(" [ COMMAND: This checks if an IP network or domain is running")
        host = input(" IP or Domain { ")

        is_up, packet_loss = self.ping_host(host)

        if is_up:
            print(f'''
 ┌─ [ COMMAND: {host} has been pinged!
 │
 └─ [ Packet loss: {packet_loss:.2f}%
            ''')
        else:
            print(f'''
 ┌─ [ COMMAND: {host} not pinged!
 └─ [ Host is not running, online, or just undetected
            ''')

        time.sleep(1)
        print(" [ COMMAND PINGER: Again? (y/n)")
        choice = input('''
  ┌─ COMMAND Pinger
  │
  └─ $ ''').lower()

        if choice == "y" or choice == "yes":
            self.tool_menu_networking_ip_pinger()
        elif choice == "n" or choice == "no":
            self.enter()
        else:
            self.tool_menu_networking_ip_pinger()

    def ping_host(self, host, count=4):
        try:
            ip_address = socket.gethostbyname(host)

            successful_pings = 0
            for _ in range(count):
                response_time = ping(ip_address)
                if response_time is not None:
                    successful_pings += 1
                time.sleep(0.5)

            if successful_pings > 0:
                packet_loss = ((count - successful_pings) / count) * 100
                return True, packet_loss

            else:
                if platform.system().lower() == "windows":
                    command = ["ping", "-n", str(count), ip_address]
                else:
                    command = ["ping", "-c", str(count), ip_address]

                output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if output.returncode == 0:
                    output_text = output.stdout.decode()
                    loss_str = "Lost = " if platform.system().lower() == "windows" else "received,"
                    lost_packets = int(output_text.split(loss_str)[-1].split(",")[0].strip().split(" ")[0])
                    packet_loss = (lost_packets / count) * 100
                    return True, packet_loss
                else:
                    return False, 100.0

        except (socket.gaierror, Exception) as e:
            print("    Error:", e)
            return False, 100.0

    def failed_auth(self):
        print("Authentication failed!")

    def enter(self):
        print("Exiting tool...")

if __name__ == "__main__":
    pinger = Pinger()
    pinger.tool_menu_networking_ip_pinger()
