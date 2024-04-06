from discord import SyncWebhook, Embed
from typing import Literal

class DiscordHook:
    def __init__(self, f_webhook_url: str):
        self.m_webhook = SyncWebhook.from_url(f_webhook_url)

    def send_message(self, f_message: str, f_title: str, f_request_response = False):
        embed = Embed(title=f_title, color=65280, description="Values in Million")
        self.m_webhook.send(content= f_message, wait= f_request_response, embed=embed)
