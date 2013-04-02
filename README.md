A full featured authentication and user system that complements django.contib.auth.


# Features

  * Class-based view implementations of all of the views
  * Invitation emailed to users, where they can complete their registration
  * Password rules

## Advanced usage

  * Override URLs and views to provide custom workflows
  * Customize views and URLs
  * Customize forms
  * Choose to not automatically log a user in after they compelte a registration, or password reset

### Messages
This app uses the [messages framework](https://docs.djangoproject.com/en/dev/ref/contrib/messages/) to pass success messages
around after certain events (password reset completion, for example). If you would like to improve the experience for
your users in this way, make sure you follow the message framework docs to enable and render these messages on your site.


# Setup & Configuration

Install this package using pip:

    pip install git+https://github.com/concentricsky/django-sky-visitor.git@v1.0#egg=django-sky-visitor

Add `'sky_visitor'` to your `INSTALLED_APPS` array.

You must specify `SECRET_KEY` in your settings for any emails with tokens to be secure (example: invitation, confirm email address, forgot password, etc)

You must at least set `LOGIN_URL` to `"login"`. You can optionally specify another valid URL or URL name of your own. Certain views in Sky Visitor depend on an accurate value for this setting and the default value in Django core (`"/authentication/login/"`) is likely invalid unless you have created it.


# Testing

Tests are broken into two separate apps running under three different "modes":

  1. "normal user" mode (default)
    * Uses `noramluser_tests/settings.py`
    * Uses `django.contrib.auth.models.User` as the user model
    * Contains the base tests
  2. "custom user" mode
    * Uses `customuser_tests/settings.py`
    * Uses `django.contrib.auth.test.custom_user.CustomUser` as the user model

A test runner is configured in each settings.py to run only the tests that are appropriate.

You can run the tests like so:

    cd example_project
    # "normal user" tests
    ./manage.py test
    # "custom user" tests
    ./manage.py test --settings=customuser_tests.settings


# Roadmap

Features to add:

  * A user should have to confirm their email address before being allowed to finalize their registration
  * Implement `LOGOUT_REDIRECT_URL`
  * Better built in password rules. Options for extending the password rules.

Improvements to documentation:

  * Write sphinx documentation
  * Step by step of password reset process and how it works
  * List all template paths that the default templates will look for


# Contributing
Please fork this repo and send pull requests. Submit issues/questions/suggestions in the [issue queue](https://github.com/concentricsky/django-sky-visitor/issues).


# Author
Built at [Concentric Sky](http://www.concentricsky.com/) by [Jeremy Blanchard](http://github.com/auzigog/).

This project is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). Copyright 2013 Concentric Sky, Inc.
