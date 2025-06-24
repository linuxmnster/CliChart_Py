import socket
import threading
from colorama import init, Fore

init(autoreset=True)

def start_client():
    try:
        print(Fore.CYAN + "\n🔗 Paste the ngrok link provided by the host.")
        raw_link = input(Fore.YELLOW + "Example (0.tcp.in.ngrok.io:12345): ").strip()

        if ":" not in raw_link:
            print(Fore.RED + "❌ Invalid format. Must be hostname:port")
            return

        host, port = raw_link.split(":")
        port = int(port)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        prompt = client.recv(1024).decode()
        print(Fore.YELLOW + prompt)
        client.send(input("> ").strip().encode())

        prompt = client.recv(1024).decode()
        if "❌" in prompt:
            print(Fore.RED + prompt)
            client.close()
            return

        print(Fore.YELLOW + prompt)
        client.send(input("> ").strip().encode())

        print(Fore.GREEN + "🟢 Connected! Type your messages below. Press Ctrl+C to exit.\n")

        def receive():
            while True:
                try:
                    msg = client.recv(1024).decode()
                    if msg:
                        print(Fore.WHITE + msg)
                except:
                    print(Fore.RED + "❌ Disconnected from server.")
                    break

        def send():
            while True:
                try:
                    msg = input()
                    client.send(msg.encode())
                except:
                    break

        threading.Thread(target=receive, daemon=True).start()
        threading.Thread(target=send, daemon=True).start()

        while True:
            pass

    except KeyboardInterrupt:
        print(Fore.RED + "\n❌ Exiting CliChat.")
        try:
            client.close()
        except:
            pass
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
