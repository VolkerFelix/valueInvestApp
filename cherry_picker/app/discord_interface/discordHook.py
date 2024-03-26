from discord import SyncWebhook
from typing import Literal

WEBHOOK_URL_PROD = "https://discord.com/api/webhooks/1222248455284723843/zDAWQaoiES9cfe2I8uCoe0gUmruQIt3R07IGtdP0ILcoTOf_TKrGGwElO6ZjA6t3MR-P"

class DiscordHook:
    def __init__(self, f_webhook_url: str):
        self.m_webhook = SyncWebhook.from_url(f_webhook_url)

    def send_message(self, f_message: str, f_request_response = False):
        self.m_webhook.send(content= f_message, wait= f_request_response)
