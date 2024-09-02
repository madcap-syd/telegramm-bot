import collections

import pytest
from github_bot.helpers.github_webhook.webhook import Webhook


def test_webhook_init(mocker, app):
    endpoint = '/endpoint'
    secret = 'secret'
    app.add_url_rule = mocker.Mock()
    webhook = Webhook(
        app=app,
        endpoint=endpoint,
        secret=secret
    )
    assert webhook._registered_hooks == collections.defaultdict(list)
    assert webhook._secret == secret.encode('utf-8')
    assert app.add_url_rule.called_once_with(
        rule=endpoint,
        endpoint=endpoint,
        view_func=webhook._webhooks_view,
        methods=['POST']
    )


def test_webhook_hock_decorator(webhook):
    event_name = 'event'

    @webhook.hook(event_name)
    def mock_fun():
        return True

    assert webhook._registered_hooks[event_name] == [mock_fun]


@pytest.mark.skip(reason='TODO: Mock request with github headers')
def test_webhook_view():
    pass


@pytest.mark.skip(reason='TODO: Mock request with github headers')
def test_webhook_get_header():
    pass
