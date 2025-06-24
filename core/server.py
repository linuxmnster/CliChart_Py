import socket
import threading
import os
from core.ngrok_handler import start_ngrok
from config import PORT
from colorama import Fore, Style, init

init(autoreset=True)

clients = {}         # username: socket
user_colors = {}     # username: color
PASSWORD = ""
log_file = None

# Define reusable color pool
color_pool = [
    Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW,
    Fore.BLUE, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX
]
color_index = 0

def get_next_color():
    global color_index
    color = color_pool[color_index % len(color_pool)]
    color_index += 1
    return color

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
    global color_index

    try:
        conn.send("Enter room password: ".encode())
        pwd = conn.recv(1024).decode().strip()
        if pwd != PASSWORD:
            conn.send("❌ Incorrect password. Connection closing.".encode())
            conn.close()
            return

        conn.send("Enter your username: ".encode())
        username = conn.recv(1024).decode().strip()

        if username in clients:
            conn.send("❌ Username already taken.".encode())
            conn.close()
            return

        # Assign color to this user
        user_colors[username] = get_next_color()
        clients[username] = conn

        join_msg = f"{Fore.GREEN}🟢 {username} has joined the chat!"
        print(join_msg)
        broadcast(join_msg)

        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            formatted = f"{user_colors[username]}{username}> {Fore.WHITE}{msg}"
            broadcast(formatted, exclude_conn=conn)

    except:
        pass
    finally:
        conn.close()
        if username in clients:
            del clients[username]
            leave_msg = f"{Fore.RED}🔴 {username} has left the chat."
            broadcast(leave_msg)
            print(leave_msg)

def kick_user(username):
    if username in clients:
        try:
            clients[username].send("You were kicked by the host.".encode())
            clients[username].close()
        except:
            pass
        del clients[username]
        broadcast(f"{Fore.MAGENTA}⚠️ {username} was kicked by the host.")

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
            cmd = input(Fore.MAGENTA)
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
