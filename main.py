import os
import sys
from core import server, client, ngrok_handler

BANNER = r"""
  ██████  ██      ██       ██████ ██   ██  █████  ████████
 ██       ██      ██      ██      ██   ██ ██   ██    ██      
 ██       ██      ██      ██      ███████ ███████    ██  
 ██       ██      ██      ██      ██   ██ ██   ██    ██      
  ██████  ███████ ██       ██████ ██   ██ ██   ██    ██
              Terminal-Based Chat Room 💬
"""

def set_ngrok_token():
    token = input("Paste your ngrok auth token: ").strip()
    os.system(f"ngrok config add-authtoken {token}")
    print("✅ Token saved!")

def show_menu():
    print(BANNER)
    print("Welcome to CliChat\n")
    print("[1] Host a Room")
    print("[2] Join a Room")
    print("[3] Set ngrok Token")
    print("[0] Exit\n")

def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            server.start_server()
        elif choice == "2":
            client.start_client()
        elif choice == "3":
            set_ngrok_token()
        elif choice == "0":
            print("Exiting CliChat. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
