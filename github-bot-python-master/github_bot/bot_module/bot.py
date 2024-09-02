# -*- coding: utf-8 -*-
from github import Github
import re
import logging

log = logging.getLogger()


class Bot(object):
    """
    Bot class that interacts with GitHub

    :param api_token API Token from Github
    :return GitHub Bot instance
    """

    is_configured = False
    bot_regex = r'@bot\s*(\S+)'

    def __init__(self, api_token):
        self.g = Github(api_token)
        self.is_configured = True
        self.commands = {
            'say-hello': self.say_hello,
            'say-goodbye': self.say_goodbye
        }

    def _get_pr_from_payload(self, payload):
        repo_id = payload['repository']['id']
        repo = self.g.get_repo(repo_id)
        issue_number = payload['issue']['number']
        return repo.get_pull(issue_number)

    def get_command_from_comment(self, payload):
        matches = re.search(self.bot_regex, str(payload['comment']['body']))
        if matches:
            command = matches.group(1)
            return command
        else:
            return None

    def execute_command_with_payload(self, command, payload):
        try:
            command_function = self.commands[command]
            command_function(payload)
        except KeyError:
            log.warning('Command not found: {}'.format(command))

    def handle_comment(self, payload):
        """
        Parses Github comment webhook
        :param payload: Webhook payload
        """
        command = self.get_command_from_comment(payload)
        if command:
            self.execute_command_with_payload(command, payload)

    def say_hello(self, payload):
        """
        Action that sends a comment from bot to the original issue (PR)

        :return Whether or not action was successfully completed
        :rtype: bool
        """
        pr = self._get_pr_from_payload(payload)
        pr.create_issue_comment('Hello world')
        #  Do here some interesting stuff with code, or any automation process
        # ...

    def say_goodbye(self, payload):
        """
        Action that sends a comment from bot to the original issue (PR)

        :return Whether or not action was successfully completed
        :rtype: bool
        """
        pr = self._get_pr_from_payload(payload)
        pr.create_issue_comment('Goodbye')
        #  Do here some interesting stuff with code, or any automation process
        # ...
