from pyngrok import ngrok, conf

def start_ngrok(port: int) -> str:
    """
    Starts an ngrok TCP tunnel on the given port and returns the public address.
    Format: 0.tcp.in.ngrok.io:PORT
    """
    try:
        # Kill any existing ngrok processes to avoid conflicts
        ngrok.kill()

        # Start a TCP tunnel on the specified port
        tunnel = ngrok.connect(port, "tcp")
        tcp_url = str(tunnel.public_url).replace("tcp://", "")

        print(f"✅ Ngrok tunnel started at: {tcp_url}")
        return tcp_url
    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")
        return "ERROR"
