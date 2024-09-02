 Github Action Bot
==================

Github bot that interacts with activated repository webhooks. You just need to activate webhooks in your repository
(or organization) and create a custom hook handler in the code to interact with Github or any other service

Main example provided in this code, reads comments from the repository Pull Requests (indicated by webhook payload) 
and looks for the bot invocation with a ``@bot do-something`` like command and performs corresponding actions.


This project also provides a best-practices template Python project which integrates several different tools.
It saves you work by setting up a number of things, including documentation, code checking, and unit test runners.

Tools included and used:

* [Paver](http://paver.github.io/paver/) for running miscellaneous tasks
* [Setuptools](http://pythonhosted.org/setuptools/merge.html) for distribution
* [Sphinx](http://sphinx-doc.org/) for documentation
* [flake8](https://pypi.python.org/pypi/flake8) for source code checking
* [pytest](http://pytest.org/latest/) for unit testing
* [mock](http://www.voidspace.org.uk/python/mock/) for mocking (not required by the template, but included anyway)
* [tox](http://testrun.org/tox/latest/) for testing on multiple Python versions



Project Setup
=============

1. Clone this repository.
2. *(Optional, but good practice)* Create a new virtual environment for your project:

With [pyenv](https://github.com/yyuu/pyenv) and [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv)

``
pyenv virtualenv my-project
pyenv local my-project
``

With [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/index.html)

`` 
mkvirtualenv my-project
``

With plain [virtualenv](http://www.virtualenv.org/en/latest/)

```
virtualenv /path/to/my-project-venv
source /path/to/my-project-venv/bin/activate
```

If you are new to virtual environments, please see the [Virtual Environment section](http://docs.python-guide.org/en/latest/dev/virtualenvs/) of Kenneth Reitz's Python Guide.


3. Install dependencies with `pip install -r requirements-dev.txt`
4. Create a ``.env`` file on project's root folder containing your secrets as follows:

``` 
GITHUB_API_TOKEN='yourverylongapitoken'
GITHUB_WEBHOOK_SECRET='yourwebhooksecret'
```


Usage Instructions
------------------

In order to run and test this Bot in your local machine, please follow first the instructions provided by
GitHub to install a custom webhook forwarder from Internet to your local machine (default port for bot is also ``4567``)

[Github Tutorial](https://developer.github.com/webhooks/configuring/)

* After the forwarder setup (if testing in local or development environment), run the application with:

``python main.py``

*Please note that this project is still in beta and Flask server has ``debug=True`` enabled for testing purposes.
 This should be removed in production environments*
 
* Define as many hook event handlers as you want in ``main.py`` using this structure:

``` python

# Defines a handler for event 'ping'
@app.webhook.hook('ping')
def on_ping(webhook_payload):
    log.info('Got ping from Github')

```

Where `ping` parameter from ``@app.webhook.hook`` decorator is the event name provided by the Github's [request header](https://developer.github.com/webhooks/#events)
and the decorated function, the one to execute with the given payload.



Using Paver
-----------

The ``pavement.py`` file comes with a number of tasks already set up for you. You can see a full list by typing ``paver help`` in the project root directory. The following are included::

    Tasks from pavement:
    lint             - Perform PEP8 style check, run PyFlakes, and run McCabe complexity metrics on the code.
    coverage         - Run tests and show test coverage report.
    test             - Run the unit tests.
    get_tasks        - Get all paver-defined tasks.
    commit           - Commit only if all the tests pass.
    test_all         - Perform a style check and run all unit tests.

For example, to run the both the unit tests and lint, run the following in the project root directory::

    paver test_all



Supported Python Versions
=========================

Github Bot PR project was developed and tested with the following versions:

* CPython 3.4, 3.6


Authors
=======

* Carlos Escura
