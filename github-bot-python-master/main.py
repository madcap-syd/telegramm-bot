#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Program entry point"""

from __future__ import print_function

import logging

from github_bot.app import App
from settings import GITHUB_API_TOKEN, GITHUB_WEBHOOK_SECRET


def init_log():
    log = logging.getLogger()
    console = logging.StreamHandler()
    format_str = '%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s'
    console.setFormatter(logging.Formatter(format_str))
    # print to console.
    log.addHandler(console)
    # Log level threshold
    log.setLevel(logging.INFO)

    return log


def main():
    """Zero-argument entry point for use with setuptools/distribute."""
    log = init_log()

    app = App(GITHUB_API_TOKEN, GITHUB_WEBHOOK_SECRET)

    # Standard Flask endpoint
    @app.flask.route('/')
    def bot_is_working():
        return "Bot is working"

    # Defines a handler for event 'ping'
    @app.webhook.hook('ping')
    def on_ping():
        log.info('Got ping from Github')

    # Defines a handler for event 'issue_comment' and others
    @app.webhook.hook('issue_comment')
    def on_issue_comment(hook_payload):
        if hook_payload['action'] in ['created', 'edited']:
            app.bot.handle_comment(hook_payload)
        else:
            log.info('No action needed, discarding webhook')

    app.flask.run(host="0.0.0.0", port=4567, debug=True)

    return app


if __name__ == '__main__':
    main()
