import os
import sys
from core import server, client, ngrok_handler
from colorama import init, Fore, Style

init(autoreset=True)

BANNER = r"""
  ██████  ██      ██       ██████ ██   ██  █████  ████████
 ██       ██      ██      ██      ██   ██ ██   ██    ██      
 ██       ██      ██      ██      ███████ ███████    ██  
 ██       ██      ██      ██      ██   ██ ██   ██    ██      
  ██████  ███████ ██       ██████ ██   ██ ██   ██    ██
              Terminal-Based Chat Room 💬
"""

def set_ngrok_token():
    token = input(Fore.YELLOW + "Paste your ngrok auth token: ").strip()
    os.system(f"ngrok config add-authtoken {token}")
    print(Fore.GREEN + "✅ Token saved!")

def show_menu():
    print(BANNER)
    print(Fore.MAGENTA + "\nWelcome to CliChat\n")
    print(Fore.YELLOW + "[1] Host a Room")
    print("[2] Join a Room")
    print("[3] Set ngrok Token")
    print("[0] Exit\n")

def main():
    while True:
        show_menu()
        choice = input(Fore.YELLOW + "Enter your choice: ").strip()
        if choice == "1":
            server.start_server()
        elif choice == "2":
            client.start_client()
        elif choice == "3":
            set_ngrok_token()
        elif choice == "0":
            print(Fore.CYAN + "Exiting CliChat. Goodbye!")
            sys.exit(0)
        else:
            print(Fore.RED + "❌ Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()