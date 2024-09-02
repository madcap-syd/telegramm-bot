# -*- coding: utf-8 -*-
import pytest

from github_bot.app import App
from settings import GITHUB_API_TOKEN, GITHUB_WEBHOOK_SECRET

parametrize = pytest.mark.parametrize


def test_on_issue_comment(create_issue_comment_payload):
    app = App(GITHUB_API_TOKEN, GITHUB_WEBHOOK_SECRET)
    app.bot.handle_comment(create_issue_comment_payload)
