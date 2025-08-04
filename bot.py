import irc.bot
import irc.connection
import datetime
import ssl
import threading
import time
import requests
from keep_alive import keep_alive

CHANNEL = "#intekk"
USERNAME = "botdynamic57"
TOKEN = "oauth:hra4zm2yrrkvophppwziermazvofew"
tracked_user = "dynamic57__"

def auto_ping():
    while True:
        try:
            requests.get("https://5046fac2-9a64-473f-abe5-2037467ea47d-00-2kk26y4sw6j6i.janeway.replit.dev/")
            print("🔁 Auto-ping wysłany!")
        except Exception as e:
            print(f"⚠️ Auto-ping error: {e}")
        time.sleep(60)

class SeenBot(irc.bot.SingleServerIRCBot):
    def __init__(self):
        print("Bot startuje...")
        server = 'irc.chat.twitch.tv'
        port = 6697

        context = ssl.create_default_context()
        factory = irc.connection.Factory(wrapper=lambda sock: context.wrap_socket(sock, server_hostname=server))

        super().__init__([(server, port, TOKEN)], USERNAME, USERNAME, connect_factory=factory)

        self.channel = CHANNEL
        self.last_seen = None

    def on_welcome(self, connection, event):
        print("✅ Połączono! Dołączam do kanału...")
        connection.join(self.channel)

