import pytest
import json

from github_bot.app import App
from github_bot.helpers.github_webhook.webhook import Webhook
from .utils import get_fixture_data

from settings import GITHUB_API_TOKEN, GITHUB_WEBHOOK_SECRET


@pytest.fixture
def create_issue_comment_payload():
    return json.loads(get_fixture_data('gh_webhook_create_issue_comment'))


@pytest.fixture
def delete_issue_comment_payload():
    return json.loads(get_fixture_data('gh_webhook_delete_issue_comment'))


@pytest.fixture
def create_issue_comment_bot_say_hello_payload():
    return json.loads(get_fixture_data('gh_webhook_create_issue_comment_bot_say_hello'))


@pytest.fixture
def create_issue_comment_bot_say_goodbye_payload():
    return json.loads(get_fixture_data('gh_webhook_delete_issue_comment_bot_say_goodbye'))


@pytest.fixture(scope='module')
def app():
    return App(GITHUB_API_TOKEN, GITHUB_WEBHOOK_SECRET)


@pytest.fixture(scope='module')
def webhook(app):
    return Webhook(
        app=app,
        endpoint='/endpoint',
        secret='secret'
    )
