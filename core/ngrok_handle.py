# core/ngrok_handler.py

from pyngrok import ngrok, conf
from colorama import Fore
import os

def start_ngrok(port: int) -> str:
    try:
        # 🔐 Read token from core/token.txt
        token_path = os.path.join(os.path.dirname(__file__), "token.txt")
        if not os.path.exists(token_path):
            print(Fore.RED + "❌ token.txt not found in core/. Please create it and paste your ngrok token inside.")
            return "ERROR"

        with open(token_path, "r") as file:
            token = file.read().strip()
            if not token:
                print(Fore.RED + "❌ token.txt is empty. Paste your ngrok token inside.")
                return "ERROR"

        # Apply token to ngrok config
        conf.get_default().auth_token = token

        # Kill previous tunnels (if any) and open new one
        ngrok.kill()
        tunnel = ngrok.connect(port, "tcp")
        public_url = str(tunnel.public_url).replace("tcp://", "")
        return public_url

    except Exception as e:
        print(Fore.RED + f"❌ Error starting ngrok: {e}")
        return "ERROR"
