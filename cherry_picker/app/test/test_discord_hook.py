import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from discord_interface.discordHook import DiscordHook

WEB_HOOK_DEV = "https://discord.com/api/webhooks/1222251474441076828/fuXu0OcHipw4Q4Q9GG1yNs8Ht5z9lWicoJLyE-b6nDEs9R_Xf1riwEurV1d9KCSPGwS4"

def test_webhook():
    hook = DiscordHook(WEB_HOOK_DEV)
    response = hook.send_message("Hello World!", f_request_response=True)
    print(str(response))
    