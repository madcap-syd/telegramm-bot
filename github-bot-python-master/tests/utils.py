import os


def get_fixture_data(data_name):
    resources = {
        'gh_webhook_create_issue_comment': 'gh/gh_webhook_create_issue_comment.json',
        'gh_webhook_delete_issue_comment': 'gh/gh_webhook_delete_issue_comment.json',
        'gh_webhook_create_issue_comment_bot_say_hello': 'gh/gh_webhook_create_issue_comment_bot_say_hello.json',
        'gh_webhook_delete_issue_comment_bot_say_goodbye': 'gh/gh_webhook_create_issue_comment_bot_say_goodbye.json'
    }
    fixture_folder_path = os.path.join(os.path.dirname(__file__), "fixtures/")
    return open(fixture_folder_path + resources[data_name]).read()
