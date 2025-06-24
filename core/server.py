import socket
import threading
import os
from core.ngrok_handler import start_ngrok
from config import PORT
from colorama import Fore, init

init(autoreset=True)

clients = {}
PASSWORD = ""
log_file = None

def broadcast(message, exclude_conn=None):
    if log_file:
        log_file.write(message + "\n")
        log_file.flush()
    for user, conn in clients.items():
        if conn != exclude_conn:
            try:
                conn.send(message.encode())
            except:
                pass

def handle_client(conn, addr):
    try:
        conn.send("Enter room password: ".encode())
        pwd = conn.recv(1024).decode().strip()
        if pwd != PASSWORD:
            conn.send(Fore.RED + "❌ Incorrect password. Connection closing.".encode())
            conn.close()
            return

        conn.send("Enter your username: ".encode())
        name = conn.recv(1024).decode().strip()

        if name in clients:
            conn.send(Fore.RED + "❌ Username already taken.".encode())
            conn.close()
            return

        clients[name] = conn
        broadcast(Fore.GREEN + f"🟢 {name} has joined the chat!")
        print(Fore.GREEN + f"[CONNECTED] {name} ({addr})")

        while True:
            msg = conn.recv(1024).decode()
            if msg == "":
                break
            broadcast(Fore.WHITE + f"{name}> {msg}", exclude_conn=conn)

    except:
        pass
    finally:
        conn.close()
        if name in clients:
            del clients[name]
            broadcast(Fore.RED + f"🔴 {name} has left the chat.")

def kick_user(username):
    if username in clients:
        try:
            clients[username].send(Fore.RED + "You were kicked by the host.".encode())
            clients[username].close()
        except:
            pass
        del clients[username]
        broadcast(Fore.MAGENTA + f"⚠️ {username} was kicked by the host.")

def start_server():
    global PASSWORD, log_file
    os.makedirs("log", exist_ok=True)
    log_file = open("log/history.txt", "a", encoding="utf-8")

    PASSWORD = input(Fore.YELLOW + "Set a password for your room: ").strip()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen()

    public_link = start_ngrok(PORT)
    print(Fore.CYAN + f"\n🔗 Share this link: {public_link}")
    print(Fore.GREEN + "🟢 Waiting for clients to join...\n")

    def accept_loop():
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

    threading.Thread(target=accept_loop, daemon=True).start()

    try:
        while True:
            cmd = input(Fore.MAGENTA + "")
            if cmd.startswith("/kick "):
                user = cmd.split(" ", 1)[1].strip()
                kick_user(user)
            elif cmd == "/exit":
                print(Fore.RED + "❌ Server shutting down.")
                for conn in clients.values():
                    conn.send("Server is shutting down.".encode())
                    conn.close()
                server_socket.close()
                log_file.close()
                break
    except KeyboardInterrupt:
        print(Fore.RED + "\n❌ Server interrupted.")
        server_socket.close()
        log_file.close()
