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
TOKEN = "oauth:qanhc55ylxwiqd5uvnrxnvwejl7klq"
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
        factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        super().__init__([(server, port, TOKEN)], USERNAME, USERNAME, connect_factory=factory)

        self.channel = CHANNEL
        self.last_seen = None

    def on_welcome(self, connection, event):
        print("✅ Połączono! Dołączam do kanału...")
        connection.join(self.channel)

    def on_join(self, connection, event):
        print(f"✅ Dołączyłem do kanału {self.channel}")

    def on_pubmsg(self, connection, event):
        user = event.source.nick.lower()
        message = event.arguments[0]
        print(f"💬 Wiadomość od {user}: {message}")

        if user == tracked_user.lower():
            self.last_seen = datetime.datetime.now()
            print(f"🕒 Zaktualizowano last_seen dla {tracked_user}")

        if message.lower().startswith("!dynamic"):
            if self.last_seen is None:
                response = "Dynamica jeszcze tu dzisiaj nie było."
            else:
                now = datetime.datetime.now()
                diff = now - self.last_seen

                days = diff.days
                hours, remainder = divmod(diff.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                parts = []
                if days > 0: parts.append(f"{days} dni")
                if hours > 0: parts.append(f"{hours} godzin")
                if minutes > 0: parts.append(f"{minutes} minut")
                if seconds > 0: parts.append(f"{seconds} sekund")
                if not parts: parts.append("0 sekund")

                diff_str = ", ".join(parts)
                timestamp = self.last_seen.strftime("(%Y-%m-%d %H:%M:%S)")
                response = f"Dynamic był tu ostatnio {diff_str} temu {timestamp}."

            print(f"📤 Wysyłam: {response}")
            connection.privmsg(self.channel, response)

if __name__ == "__main__":
    keep_alive()
    threading.Thread(target=auto_ping, daemon=True).start()
    bot = SeenBot()
    bot.start()