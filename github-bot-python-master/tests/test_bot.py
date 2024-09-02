# -*- coding: utf-8 -*-
import pytest
import vcr

from github_bot.bot_module.bot import Bot
from settings import GITHUB_API_TOKEN
from tests.conftest import create_issue_comment_bot_say_hello_payload, create_issue_comment_bot_say_goodbye_payload, \
    create_issue_comment_payload

my_vcr = vcr.VCR(record_mode='once')


@pytest.fixture(scope='module')
def bot():
    return Bot(GITHUB_API_TOKEN)


def test_bot_init(bot):
    assert bot.is_configured
    assert set(bot.commands.keys()) == {'say-hello', 'say-goodbye'}


# TODO: Migrate to vcrpy --> https://github.com/kevin1024/vcrpy/issues/227
def test_bot_get_pr_from_payload(bot, create_issue_comment_payload):
    pr = bot._get_pr_from_payload(create_issue_comment_payload)
    assert pr.id == 172572812


# TODO: Use cassette
@pytest.mark.parametrize("expected_command, payload", [
    (None, create_issue_comment_payload()),
    ('say-hello', create_issue_comment_bot_say_hello_payload()),
    ('say-goodbye', create_issue_comment_bot_say_goodbye_payload())
])
def test_bot_get_command_from_comment(bot, expected_command, payload):
    command = bot.get_command_from_comment(payload)
    assert command == expected_command


@pytest.mark.parametrize("command,payload", [
    ('say-hello', create_issue_comment_bot_say_hello_payload()),
    ('say-goodbye', create_issue_comment_bot_say_goodbye_payload())
])
def test_handle_comment(mocker, bot, command, payload):
    bot.commands[command] = mocker.Mock()
    bot.handle_comment(payload)
    assert bot.commands[command].called_once


@pytest.mark.parametrize("command,payload", [
    ('say-hello', create_issue_comment_bot_say_hello_payload()),
    ('say-goodbye', create_issue_comment_bot_say_goodbye_payload())
])
def test_execute_command_with_payload(mocker, bot, command, payload):
    mock = mocker.Mock()
    bot.commands[command] = mock
    bot.execute_command_with_payload(command, payload)
    assert mock.called_once


def test_execute_command_with_payload_no_exists(bot):
    # Ignore the command when the command doesn't exist
    bot.execute_command_with_payload('unknown-command', {})


# TODO: Use cassette to record Github request
def test_bot_say_hello(mocker, bot, create_issue_comment_bot_say_hello_payload):
    pr_mock = mocker.Mock()
    pr_mock.create_issue_comment = mocker.Mock()
    _get_pr_from_payload_mock = mocker.Mock(return_value=pr_mock)
    bot._get_pr_from_payload = _get_pr_from_payload_mock
    bot.say_hello(create_issue_comment_bot_say_hello_payload)
    assert _get_pr_from_payload_mock.called_once
    assert pr_mock.create_issue_comment.called_once_with('Hello world')


# TODO: Use cassette to record Github request
def test_bot_say_goodbye(mocker, bot, create_issue_comment_bot_say_goodbye_payload):
    pr_mock = mocker.Mock()
    pr_mock.create_issue_comment = mocker.Mock()
    _get_pr_from_payload_mock = mocker.Mock(return_value=pr_mock)
    bot._get_pr_from_payload = _get_pr_from_payload_mock
    bot.say_goodbye(create_issue_comment_bot_say_goodbye_payload)
    assert _get_pr_from_payload_mock.called_once
    assert pr_mock.create_issue_comment.called_once_with('Goodbye')
