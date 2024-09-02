import collections
import hashlib
import hmac

import six
from flask import abort, request


class Webhook(object):
    """
    Create a webhook endpoint on a given Flask app

    :param app: Flask app running in the project
    :param endpoint: webhook URL endpoint
    :param secret: (optional) Secret used to authenticate Github's request
    """

    def __init__(self, app, endpoint='/webhooks', secret=None):
        app.add_url_rule(rule=endpoint,
                         endpoint=endpoint,
                         view_func=self._webhooks_view,
                         methods=['POST'])

        self._registered_hooks = collections.defaultdict(list)
        if secret is not None and not isinstance(secret, six.binary_type):
            secret = secret.encode('utf-8')
        self._secret = secret

    def hook(self, event_type):
        """
        Registers a hook function as a class decorator and therefore,
        multiple hooks can be registered

        :param event_type: Event name from GitHub event_names list.
        :type event_type: str
        """

        def decorator(func):
            self._registered_hooks[event_type].append(func)
            return func

        return decorator

    def _webhooks_view(self):
        """
        Main function invoked from Flask once endpoint is reached
        """

        digest = None

        if self._secret:
            digest = hmac.new(self._secret, request.data, hashlib.sha1).hexdigest()

        if digest is not None:
            signature_comp = self._get_header('X-Hub-Signature').split('=', 1)
            if not isinstance(digest, six.text_type):
                digest = six.text_type(digest)

            if not hmac.compare_digest(signature_comp[1], digest):
                abort(400, 'Invalid signature')

        data = request.get_json()
        if data is None:
            abort(400, 'Request body must contain json')

        event_type = self._get_header('X-Github-Event')

        # Dispatch all hook functions
        for hook in self._registered_hooks.get(event_type, []):
            hook(data)

        # Returned a 202 as many hooks could have been triggered
        return 'OK', 202

    @staticmethod
    def _get_header(key):
        """Get header from a given key

        :param key: Key to search for
        """

        try:
            return request.headers[key]
        except KeyError:
            abort(400, 'Missing header: ' + key)
