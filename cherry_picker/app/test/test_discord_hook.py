import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from discord_interface.discordHook import DiscordHook

WEB_HOOK_DEV = "https://discord.com/api/webhooks/1224779729136255128/ACRhjlv6NED9_H-g6_0oTgWH7EMwt_PObry403HCSjWb5u79PGOcnjfyTli_7GztV4tT"

def test_webhook():
    hook = DiscordHook(WEB_HOOK_DEV)
    response = hook.send_message("Hello World!", "Test", f_request_response=True)
    print(str(response))
    