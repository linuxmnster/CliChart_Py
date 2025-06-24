import socket
import threading

def start_client():
    try:
        print("\n🔗 Paste the ngrok link provided by the host.")
        raw_link = input("Example (0.tcp.in.ngrok.io:12345): ").strip()

        if ":" not in raw_link:
            print("❌ Invalid format. Must be hostname:port")
            return

        host, port = raw_link.split(":")
        port = int(port)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        # Receive room password prompt
        prompt = client.recv(1024).decode()
        print(prompt)
        client.send(input("> ").strip().encode())

        # Receive username prompt or error
        prompt = client.recv(1024).decode()
        if "❌" in prompt:
            print(prompt)
            client.close()
            return

        print(prompt)
        client.send(input("> ").strip().encode())

        print("🟢 Connected! Type your messages below. Press Ctrl+C to exit.\n")

        # Thread to receive messages
        def receive():
            while True:
                try:
                    msg = client.recv(1024).decode()
                    if msg:
                        print(msg)
                except:
                    print("❌ Disconnected from server.")
                    break

        # Thread to send messages
        def send():
            while True:
                try:
                    msg = input()
                    client.send(msg.encode())
                except:
                    break

        threading.Thread(target=receive, daemon=True).start()
        threading.Thread(target=send, daemon=True).start()

        # Keep the main thread alive
        while True:
            pass

    except KeyboardInterrupt:
        print("\n❌ Exiting CliChat.")
        try:
            client.close()
        except:
            pass
    except Exception as e:
        print(f"❌ Error: {e}")
