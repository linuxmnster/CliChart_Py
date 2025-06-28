import os
import sys
from core import server, client
from colorama import init, Fore
from pyfiglet import figlet_format

init(autoreset=True)

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def get_banner():
    return Fore.CYAN + figlet_format("ShellSpace", font="slant") + Fore.YELLOW + "\nTerminal-Based Chat Room 💬\n"

def set_ngrok_token():
    token = input(Fore.YELLOW + "Paste your ngrok auth token: ").strip()
    os.system(f"ngrok config add-authtoken {token}")
    print(Fore.GREEN + "✅ Token saved!")

def show_menu():
    print(get_banner())
    print(Fore.YELLOW + "[1] Host a Room")
    print("[2] Join a Room")
    print("[3] Set ngrok Token")
    print("[4] Clear Terminal")
    print("[0] Exit\n")

def main():
    while True:
        show_menu()
        choice = input(Fore.GREEN + "Enter your choice: ").strip()
        if choice == "1":
            server.start_server()
        elif choice == "2":
            client.start_client()
        elif choice == "3":
            set_ngrok_token()
        elif choice == "4":
            clear_terminal()
        elif choice == "0":
            print(Fore.CYAN + "👋 Exiting ShellSpace. Goodbye!")
            sys.exit(0)
        else:
            print(Fore.RED + "❌ Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
