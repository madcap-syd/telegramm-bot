# -*- coding: utf-8 -*-
from __future__ import print_function

from github_bot.helpers.github_webhook.webhook import Webhook
from flask import Flask

from .bot_module.bot import Bot


class App():
    def __init__(self, github_api_token, github_webhook_secret):
        # Create bot and configure  it
        self.bot = Bot(github_api_token)

        # Standard Flask app
        self.flask = Flask(__name__)

        # Defines '/webhooks' endpoint
        self.webhook = Webhook(self.flask, secret=github_webhook_secret)
