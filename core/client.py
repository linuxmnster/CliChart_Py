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

        # Password authentication
        prompt = client.recv(1024).decode()
        print(Fore.YELLOW + prompt)
        client.send(input(Fore.YELLOW + "> ").strip().encode())

        # Username
        prompt = client.recv(1024).decode()
        if "❌" in prompt:
            print(Fore.RED + prompt)
            client.close()
            return

        print(Fore.YELLOW + prompt)
        username = input(Fore.YELLOW + "> ").strip()
        client.send(username.encode())

        print(Fore.GREEN + "🟢 Connected! Type your messages below.")
        print(Fore.MAGENTA + "📌 Type '/leave' to exit the chat.\n")

        stop_flag = threading.Event()

        def receive():
            while not stop_flag.is_set():
                try:
                    msg = client.recv(1024).decode()
                    if msg:
                        print("\r" + Fore.WHITE + msg + "\n" + Fore.YELLOW + f"{username}> ", end="")
                    else:
                        break
                except:
                    print(Fore.RED + "\n❌ Disconnected from server.")
                    break

        def send():
            while not stop_flag.is_set():
                try:
                    msg = input(Fore.YELLOW + f"{username}> ")
                    if msg.strip().lower() == "/leave":
                        print(Fore.RED + "🚪 You left the chat.")
                        client.send(f"{username} has left the chat.".encode())
                        client.close()
                        stop_flag.set()
                        break
                    client.send(msg.encode())
                except:
                    break

        threading.Thread(target=receive, daemon=True).start()
        threading.Thread(target=send, daemon=True).start()

        while not stop_flag.is_set():
            pass

    except KeyboardInterrupt:
        print(Fore.RED + "\n❌ Exiting CliChat.")
        try:
            client.close()
        except:
            pass
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
