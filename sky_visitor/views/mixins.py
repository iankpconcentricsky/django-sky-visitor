# Copyright 2012 Concentric Sky, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.utils.http import base36_to_int
from sky_visitor.emails import TokenTemplateEmail


class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class SendTokenEmailMixin(object):
    email_template_class = TokenTemplateEmail

    def get_email_kwargs(self, user):
        return {'user': user}

    def send_email(self, user):
        email_template = self.email_template_class(**self.get_email_kwargs(user))
        return email_template.send_email()


class TokenValidateMixin(object):
    token_generator = default_token_generator
    display_message_on_invalid_token = True
    is_token_valid = False
    invalid_token_message = "This one-time use URL has already been used. Try to login or use the forgot password form."

    def get_token_generator(self):
        return self.token_generator

    def dispatch(self, request, *args, **kwargs):
        UserModel = get_user_model()
        uidb36 = kwargs['uidb36']
        token = kwargs['token']
        assert uidb36 is not None and token is not None  # checked by URLconf
        try:
            uid_int = base36_to_int(uidb36)
            # Get an AuthUser instance here since we don't need any of the extra aspects of the SubclassedUser
            self._user = UserModel._default_manager.get(id=uid_int)
        except (ValueError, OverflowError, UserModel.DoesNotExist):
            self._user = None
        self.is_token_valid = (self._user is not None and self.get_token_generator().check_token(self._user, token))
        if not self.is_token_valid:
            return self.token_invalid(request, *args, **kwargs)
        return super(TokenValidateMixin, self).dispatch(request, *args, **kwargs)

    def token_invalid(self, request, *args, **kwargs):
        if self.display_message_on_invalid_token:
            messages.error(request, self.invalid_token_message, fail_silently=True)
        return HttpResponseRedirect(resolve_url(settings.LOGIN_URL))

    def get_user_from_token(self):
        return self._user
