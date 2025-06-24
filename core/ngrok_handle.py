from pyngrok import ngrok
from colorama import Fore, init

init(autoreset=True)

def start_ngrok(port: int) -> str:
    try:
        ngrok.kill()
        tunnel = ngrok.connect(port, "tcp")
        return str(tunnel.public_url).replace("tcp://", "")
    except Exception as e:
        print(Fore.RED + f"❌ Error starting ngrok: {e}")
        return "ERROR"
